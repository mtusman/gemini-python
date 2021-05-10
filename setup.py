from setuptools import setup

setup(
    name='gemini-python',
    version='0.2.1',
    packages=['gemini'],
    url='https://github.com/mtusman/gemini-python',
    license='MIT',
    author='Mohammad Usman',
    author_email='m.t.usman@hotmail.com',
    description='A python client for the Gemini API and Websocket',
    python_requires='>=3',
    install_requires=['requests', 'pytest', 'websocket', 'websocket-client'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords=['gemini', 'bitcoin', 'bitcoin-exchange', 'ethereum', 'ether', 'BTC', 'ETH', 'gemini-exchange'],
)
