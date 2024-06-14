# How to update the documentation version

After every new release of Acquire Python, the documentation version needs
to be manually updated. This can be done by issuing the following command on the
root of the Acquire docs repository:

```bash
mike deploy --push --update-aliases <version-tag> stable
```

where `<version-tag>` is the tag of the new release. This will

- create/update the alias `stable` for the `<version-tag>` release of the docs;
- update the version switcher dropdown accordingly (autogenerating the
  `versions.json` file, which is only present in the deployed pages), and
- deploy the new version of the documentation to the `gh-pages` branch of the
  repository (if the `--push` option is used, as above.)

The default version of the documentation pages is `stable`, but this can be
changed to another version by using the `mike set-default <identifier>` command.

!!! note

    In order to provide downloadable `.py` files to the tutorials, make sure
    you run `bash .github/workflows/convert.sh` before deploying a new version
    with `mike`.
