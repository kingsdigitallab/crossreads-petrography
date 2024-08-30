from . import *
from datetime import datetime

class CrossreadsPetrographyTool:
    name=None
    
    def __init__(
            self,
            path=None,
            path_input=None,
            path_output=None,
            **path_kwargs
            ):
        assert self.name
        paths = {
            k[len(self.name)+1:] if k[len(self.name)+1:] else self.name: v
            for k, v in config.paths.items()
            if k.startswith(f"{self.name}")
        }
        if path:
            paths[self.name] = path
        if path_input:
            paths[f"input"] = path_input
        if path_output:
            paths[f"output"] = path_output
        for k, v in path_kwargs.items():
            if k.startswith("path_") and v:
                paths[k[5:]] = v
        self.paths = paths


    def __getattr__(self, key):
        if key.startswith('path'):
            return self.paths[key[5:] if key!='path' else self.name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")


    
    def __repr__(self):
        paths = {f'path_{k}' if k!=self.name else 'path': v for k, v in self.paths.items()}
        pathstr = '\n'.join([f'    {k} = "{v}",' for k, v in paths.items()])
        return f"{self.__class__.__name__}(\n{pathstr}\n)"

    @property
    def output_path_now(self):
        return os.path.join(self.paths['output'], datetime.now().strftime('%Y-%m-%d'))
    
    def run(self):
        raise NotImplementedError("Subclass must implement abstract method")
    
    def save(self):
        raise NotImplementedError("Subclass must implement abstract method")
    