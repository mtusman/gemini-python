from setuptools import setup

with open('README.md') as f:
    readme = f.read()

setup(
    name='gemini',
    version='0.2.0',
    packages=['gemini'],
    url='https://github.com/mtusman/gemini-python-wrapper',
    license='MIT',
    author='Mohammad Usman',
    author_email='m.t.usman@hotmail.com',
    long_description=readme,
    description='A python client for the Gemini API',
    python_requires='>=3',
    install_requires=['requests', 'pytest', 'websocket', 'websocket-client'],
    keywords=['gemini', 'bitcoin', 'bitcoin-exchange', 'ethereum', 'ether', 'BTC', 'ETH', 'gemini-exchange'],
)
