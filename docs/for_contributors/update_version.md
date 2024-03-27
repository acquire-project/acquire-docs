# How to update the documentation version

After every new release of Acquire Python, the documentation version needs
to be updated. This can be done by issuing the following command on the root of
the Acquire docs repository:

```bash
mike deploy --push --update-aliases <version-tag> stable
```

where `<version-tag>` is the tag of the new release. This will create a new
alias for the `<version-tag>` release as `stable`, update the version switcher
dropdown accordingly, and deploy the new version of the documentation to the
`gh-pages` branch of the repository.

The default version of the documentation pages is `stable`, but this can be
changed by editing the `mkdocs.yml` file.
