import importlib.util
import inspect
import os
from pathlib import Path
from typing import Callable, Tuple, Type

from pytexresume.infos import Info
from pytexresume.resume import BasicResume, SContainer


def load_template_module(template_name: str, headers_file):
    template_root = Path(__file__).parent / template_name
    resume_file = template_root / "resume.py"

    if not resume_file.exists():
        print(f"No resume.py found in {template_name}. Skipping.")
        return

    # module_name = f"{template_name}_resume"
    spec = importlib.util.spec_from_file_location(template_name, resume_file)
    if spec is None:
        raise ImportError(f"Cannot find module {template_name} at {resume_file}")

    module = importlib.util.module_from_spec(spec)
    # sys.modules[template_name] = module
    spec.loader.exec_module(module)
    print(f"Module {template_name} loaded from {resume_file}")

    for _, cls in inspect.getmembers(module, inspect.isclass):
        if issubclass(cls, BasicResume) and cls is not BasicResume:
            TemplateSet.register_template_class(cls, template_name, headers_file)


class TemplateSet:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TemplateSet, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        self.templates = {}
        self.template_cls = {}
        self.generators = {}
        self.load_all_templates()

    def load_all_templates(self):
        template_root = Path(__file__).parent
        fes = os.listdir(template_root)
        for fe in fes:
            fed = template_root / fe
            if fed.is_dir() and not fe.startswith("_"):
                headers_file = fed / "headers.yaml"
                self.templates[fe] = headers_file
                load_template_module(fe, headers_file)
                print(f"template {fe} loaded.")

    def reload(self): return self.load_all_templates()

    @staticmethod
    def register_template_class(cls: Type[BasicResume], template_name: str, headers_file):
        methods = inspect.getmembers(cls, predicate=inspect.isfunction)
        original_init = cls.__init__

        def new_init(self, *args, **kwargs):
            if 'heads_config' in kwargs:
                kwargs['heads_config'] = headers_file
            else:
                args = (headers_file,) + args
            original_init(self, *args, **kwargs)
        cls.__init__ = new_init
        template_generators = {}
        for name, method in methods:
            signature = inspect.signature(method)
            if issubclass(signature.return_annotation, SContainer):
                if len(signature.parameters) == 2:
                    signs = list(signature.parameters.items())
                    _self, _ = signs[0]
                    _, _para_param = signs[1]
                    if _self == "self" and issubclass(_para_param.annotation, Info):
                        template_generators[_para_param.annotation.__name__] = (_para_param.annotation, name)
        TemplateSet._instance.generators[template_name] = template_generators
        TemplateSet._instance.template_cls[template_name] = cls

    def get_template(self, template_name: str) -> Type[BasicResume]: return self.template_cls.get(template_name)

    def get_generator(self, instance: BasicResume, template_name: str, input_type_name: str) -> Tuple[Type[Info], Callable[[Info], SContainer]]:
        para_cls, para_call_name = self.generators[template_name][input_type_name]
        return para_cls, getattr(instance, para_call_name)


Template = TemplateSet()
