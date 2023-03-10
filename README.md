# infra-tests
Repository for infrastructure &amp; runtime integration tests (both applications and test harness)

# Running Tests

## Installing dependencies

1. Install `pipenv` if you don't already have it. (On Macs: `brew install pipenv`)
2. Run:
   ```
   pipenv install
   ```
   This will create a virtualenv for you, and install dependendencies into it.

## Running locally

* You must have an executable `klotho_main` at the root of this package (or a symlink to it).
* You may (optionally) have an executable `klotho_release` at the root of this package. If you do not, the runner will download the latest release and use that.

You can kick off individual runs with:

```bash
pipenv run tests ...
```

Example:
```
pipenv run tests --directories ts-app --region us-west-1 --provider aws
```

To load an interactive pipenv environment:

```bash
pipenv shell
```

Example:
```
$ pipenv shell
$ python3.10 runner/runner.py --directories ts-app --region us-west-1 --provider aws
```
