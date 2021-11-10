import os
import glob
from distutils.dir_util import copy_tree

import lava
import lava.lib.dl.slayer as slayer
import lava.lib.dl.bootstrap as bootstrap


tutorial_list = [  # list of all notebooks to sync
    {
        'module': lava,
        'dst': 'lava/notebooks/',
        'tutorials': {
            'end_to_end': 'End to end tutorials',
        },
    },
    {
        'module': slayer,
        'dst': 'lava-lib-dl/slayer/notebooks/',
        'tutorials': {
            'oxford': 'Oxford spike train regression',
            'nmnist': 'NMNIST digit classification',
            'pilotnet': 'PilotNet steering angle prediction',
            'neuron_dynamics': 'Dynamics and Neurons',
        },
    },
    {
        'module': bootstrap,
        'dst': 'lava-lib-dl/bootstrap/notebooks/',
        'tutorials': {
            'mnist': 'MNIST digit classification',
        },
    },
]


def create_nb_rst(folder_path, rst_name, header, ignore=[]):
    """Create rST file for notebook.

    Parameters
    ----------
    nb_path : str
        notebook path
    rst_name : str
        rST file name
    header : str
        header of the rST file entry
    """
    rst_text = f'''
    {header}
    {"="*len(header)}

    .. toctree::
        :maxdepth: 1
        :glob:

    '''.replace('\n' + ' '*4, '\n')

    nb_paths = glob.glob(folder_path + '/*.ipynb')
    for nb_path in nb_paths:
        _, nb_name = nb_path.rsplit('/', 1)
        if nb_name in ignore:
            print(nb_name, ignore)
            continue
        rst_text += f'    {nb_name}{os.linesep}'

    with open(folder_path + '/' + rst_name, 'wt') as f:
        f.write(rst_text)


if __name__ == '__main__':
    for tutorials in tutorial_list:
        module = tutorials['module']
        module_path = module.__path__[0]
        module_path = module_path.split('src/lava')[0]
        if module_path[-1] != '/':  # this is temp before lava dir restructure
            module_path += '/'
        dst = tutorials['dst']
        if 'ignore' in tutorials.keys():
            ignore = tutorials['ignore']
        else:
            ignore = []
        os.makedirs(dst, exist_ok=True)
        for tutorial, header in tutorials['tutorials'].items():
            src_path = glob.glob(
                f'{module_path}tutorials/**/{tutorial}',
                recursive=True,
            )
            dst_path = dst + tutorial
            if len(src_path) == 1:
                src_path = src_path[0]
                print(f'copying from {src_path} to {dst_path}')
                copy_tree(src_path, dst_path)
                create_nb_rst(src_path, tutorial+'.rst', header, ignore)
            else:
                if len(src_path) == 0:
                    print(f'search path: {module_path}tutorials/**/{tutorial}')
                    raise Exception('Module not found! Check your config')
                else:
                    raise Exception(
                        f'Multiple Moudles found: '
                        f'{src_path}'
                    )
