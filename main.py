import os
import logging
import prompt_manager
import argparse
import yaml

from prompts import (
    SYSTEM_PROMPT,
    MODELS_PROMPT,
    DONE,
    NEXT,
    SERIALIZERS_PROMPT,
    ADMIN_PROMPT,
    APPS_PROMPT,
    SETTINGS_PROMPT,
)

logging.basicConfig(level=os.environ.get("LOG_LEVEL", logging.INFO))
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise EnvironmentError("Could not find OPENAI_API_KEY in environment variables")

log = logging.getLogger(__name__)


def create_file(location, content):
    directory = os.path.dirname(os.path.abspath(location))

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(location, "w") as f:
        f.write(content)


def generate_files(pm, base_path, prompt):
    pm.add_message(role="user", content=prompt)

    while True:
        res = pm.generate()

        if res == DONE:
            break

        lines = res.split("\n")
        file_location = lines[0]
        file_content = "\n".join(lines[1:])

        path = os.path.join(base_path, file_location)
        create_file(location=path, content=file_content)

        pm.add_message(role="user", content=NEXT)


def finish_setup(base_path):
    directories = []
    for root, dirs, files in os.walk(base_path):
        for d in dirs:
            directories.append(os.path.join(root, d, "__init__.py"))
            directories.append(os.path.join(root, d, "migrations", "__init__.py"))

    for d in directories:
        create_file(d, content="")
        create_file(d, content="")


def main(definition, base_path, project_name):
    with open(definition, "r") as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)

    log.info("Setting up prompt manager")
    pm = prompt_manager.PromptManager()
    pm.add_message(role="system", content=SYSTEM_PROMPT)

    log.info("Generating models")
    generate_files(pm=pm, base_path=base_path, prompt=MODELS_PROMPT.format(yaml=data))

    log.info("Generating app configs")
    generate_files(pm=pm, base_path=base_path, prompt=APPS_PROMPT.format(yaml=data))

    log.info("Generating serializers")
    generate_files(pm=pm, base_path=base_path, prompt=SERIALIZERS_PROMPT)

    log.info("Generating admin files")
    generate_files(pm=pm, base_path=base_path, prompt=ADMIN_PROMPT)

    log.info("Updating settings...")

    with open(os.path.join(base_path, project_name, "settings.py"), "r+") as file:
        pm.add_message(role="user", content=SETTINGS_PROMPT.format(content=file.read()))
        settings_file = pm.generate()

        file.seek(0)
        file.write(settings_file)
        file.truncate()

    log.info("All done!")

    finish_setup(base_path=base_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A program to do something with a given definition file."
    )
    parser.add_argument(
        "--definition", type=str, help="The path to the definition file.", required=True
    )
    parser.add_argument(
        "--output",
        type=str,
        help="The path to the root of the Django project",
        required=True,
    )
    parser.add_argument(
        "--project_name",
        type=str,
        help="The project name used when setting up Django",
        required=True,
    )

    args = parser.parse_args()

    main(
        definition=args.definition,
        base_path=args.output,
        project_name=args.project_name,
    )
