from setuptools import setup

with open('README.md') as f:
    readme = f.read()

setup(
    name='gemini-python-wrapper',
    version='0.0.1',
    packages=['gemini-python-wrapper'],
    url='https://github.com/mtusman/gemini-python-wrapper',
    license='MIT',
    author='Mohammad Usman',
    author_email='m.t.usman@hotmail.com',
    zip_safe=False,
    long_description=readme,
    description='A python client for the Gemini API',
    keywords=['gemini', 'bitcoin', 'bitcoin-exchange', 'ethereum', 'ether', 'BTC', 'ETH', 'gemini-exchange'],
)
