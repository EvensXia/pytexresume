from pathlib import Path

import yaml
from pylatex import Command, Document, NoEscape, Package


def no_escape_str(args): return NoEscape(args)


def no_escape_list(*args): return [no_escape_str(i) for i in args]


def no_escape_dict(**kwargs): return {k: no_escape_list(*v) if isinstance(v, list)
                                      else no_escape_str(v) for k, v in kwargs.items()}


class Doc:
    def __init__(self, heads_config: str | Path):
        with open(heads_config, "r") as f:
            config: dict = yaml.safe_load(f)

        document_cfg: dict = config.get("Document", {})
        self.doc = Document(**document_cfg)

        package_cfg: dict = config.get("Package", {})
        for key, val_cfg in package_cfg.items():
            if isinstance(val_cfg, dict):
                self.doc.packages.append(Package(key, **val_cfg))
            else:
                self.doc.packages.append(Package(key))

        # 添加命令
        command_cfg: list = config.get("Command", [])
        for cmds in command_cfg:
            if isinstance(cmds, list):
                self.doc.preamble.append(Command(*no_escape_list(*cmds)))
            elif isinstance(cmds, dict):
                self.doc.preamble.append(Command(**no_escape_dict(**cmds)))
            elif isinstance(cmds, str):
                self.doc.preamble.append(Command(*no_escape_list(*cmds.split())))
            else:
                continue

        custom_commands: dict = config.get("CustomCommands", {})
        for cmd_name, cmd_def in custom_commands.items():
            self.doc.preamble.append(NoEscape(
                '\\newcommand{'
                + cmd_name
                + '}['
                + str(cmd_def["args"])
                + ']{'
                + cmd_def["cmd"]
                + '}'
            ))

    def generate_pdf(self, filename): self.doc.generate_pdf(filename, clean_tex=False)
