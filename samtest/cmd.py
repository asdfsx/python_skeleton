from __future__ import print_function

import argparse
from stevedore import extension
from stevedore import driver

def driver_mode(parsed_args, data):
    mgr = driver.DriverManager(
        namespace='stevedore.example.formatter',
        name=parsed_args.format,
        invoke_on_load=True,
        invoke_args=(parsed_args.width,),
    )
    for chunk in mgr.driver.format(data):
        print(chunk, end='')

def extension_mode(parsed_args, data):
    mgr = extension.ExtensionManager(
        namespace='stevedore.example.formatter',
        invoke_on_load=True,
        invoke_args=(parsed_args.width,),
    )

    def format_data(ext, data):
        return (ext.name, ext.obj.format(data))

    results = mgr.map(format_data, data)

    for name, result in results:
        print('Formatter: {0}'.format(name))
        for chunk in result:
            print(chunk, end='')
        print('')

def main():
    print("=========samtest.cmd.main===========")

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--format',
        nargs='?',
        default=None,
        help='the output format',
    )
    parser.add_argument(
        '--width',
        default=60,
        type=int,
        help='maximum output width for text',
    )
    parsed_args = parser.parse_args()

    data = {
        'a': 'A',
        'b': 'B',
        'long': 'word ' * 80,
    }

    if parsed_args.format is None:
        extension_mode(parsed_args, data)
    else:
        driver_mode(parsed_args, data)

if __name__ == "__main__":
    main()
