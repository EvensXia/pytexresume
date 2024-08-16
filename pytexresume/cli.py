import argparse
import os
import subprocess
import sys
from pprint import pprint

import yaml
from pytexresume.resume import BasicResume
from pytexresume.templates import Template


def gen(file):
    with open(file) as f:
        config: dict = yaml.safe_load(f)

    TEMPLATES = config.get("TEMPLATES", [])
    OUTPUT = config.get("OUTPUT", "resume")
    for template in TEMPLATES:
        inst: BasicResume = Template.get_template(template)()
        for call_key, value in config.get("RESUME", {}).items():
            info_parser, calling_func = Template.get_generator(inst, template, call_key)
            block = calling_func(info_parser.load(value))
            inst.doc.append(block)
        inst.generate_pdf(f"{OUTPUT}_{template}")


def list_templates(): pprint(Template.templates)


def install_templates(template_repo):
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    repo_name = template_repo.split("/")[-1].replace(".git", "")

    # Clone the GitHub repository into the templates directory
    try:
        from git import Repo
        clone_path = os.path.join(templates_dir, repo_name)
        print(f"Cloning {template_repo} into {clone_path}...")
        Repo.clone_from(template_repo, clone_path)
        print(f"Successfully cloned {template_repo}")

        # Check if requirements.txt exists and install dependencies if found
        requirements_path = os.path.join(clone_path, 'requirements.txt')
        if os.path.exists(requirements_path):
            print(f"Found requirements.txt in {repo_name}, installing dependencies...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
            print(f"Dependencies installed successfully.")
        else:
            print(f"No requirements.txt found in {repo_name}, skipping dependency installation.")

    except Exception as e:
        print(f"Failed to clone {template_repo}: {e}")


def remove_templates(template_name):
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    template_path = os.path.join(templates_dir, template_name)

    if os.path.exists(template_path):
        print(f"Removing template {template_name}...")
        subprocess.call(['rm', '-rf', template_path])
        print(f"Template {template_name} removed successfully.")
    else:
        print(f"Template {template_name} does not exist.")


def main():
    parser = argparse.ArgumentParser(description="Resume CLI Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # gen 子命令
    gen_parser = subparsers.add_parser("gen", help="Generate resume from a YAML file")
    gen_parser.add_argument("file", help="Path to the YAML file")

    # list 子命令
    subparsers.add_parser("list", help="List available templates")

    # install 子命令
    install_parser = subparsers.add_parser("install", help="Install a template")
    install_parser.add_argument("template", help="Name of the template to install")

    # remove 子命令
    remove_parser = subparsers.add_parser("remove", help="Remove a template")
    remove_parser.add_argument("template", help="Name of the template to remove")

    # 解析命令行参数
    args = parser.parse_args()

    # 根据命令执行相应的函数
    if args.command == "gen":
        gen(args.file)
    elif args.command == "list":
        list_templates()
    elif args.command == "install":
        install_templates(args.template)
    elif args.command == "remove":
        remove_templates(args.template)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
