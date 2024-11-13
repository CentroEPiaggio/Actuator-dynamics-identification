from setuptools import find_packages, setup

package_name = 'identification_process'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='francesco iotti',
    maintainer_email='f.iotti@studenti.unipi.it',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'my_node = identification_process.my_node:main',
            'impulse = identification_process.impulse:main',
            'step = identification_process.step:main',
            'sine_wave = identification_process.sinewave:main'

        ],
    },
)
