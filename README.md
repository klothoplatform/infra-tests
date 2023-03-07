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

You must have 2 binaries present at the root of this package
* klotho_main - the mainline versions of klotho you want to test
* klotho_release - the released version of klotho you want to test

To load your pipenv environment:

```bash
pipenv shell
```

```
$ python3.10 runner/runner.py --help
Usage: runner.py [OPTIONS]

Options:
  --directories TEXT    The directories to be compiled  [required]
  --region TEXT         The region to deploy to  [required]
  --disable-tests TEXT  The tests to be disabled
  --provider TEXT       The provider to test  [required]
  --help                Show this message and exit.
  ```

Example:
```
python3.10 runner/runner.py --directories ts-app --region us-west-1 --provider aws
```
