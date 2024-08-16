# PyTexResume

PyTexResume is a Python-based resume generator that utilizes LaTeX for high-quality, customizable PDF output. It supports the installation and management of templates from GitHub repositories and provides a simple CLI for generating resumes based on YAML configuration files.

## Features

- Generate professional resumes using LaTeX templates.
- Supports multiple templates and easy switching.
- Install and manage resume templates from remote repositories.
- YAML-based configuration for defining resume content.


## Installation

```bash
apt install texlive-full # texlive-full is needed
python -m pip install pytexresume
```

## Usage

```bash
pytexresume list  # list all templates
pytexresume install # install template from git link
pytexresume remove # remove template installed
pytexresume gen /path/to/your/resume.yaml # as assets/example.yaml
```

## Resume

see [assets/example.yaml](assets/example.yaml)

## Template

create your own Template as [pytexresume/templates/en_simple](pytexresume/templates/en_simple)