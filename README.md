# mycicd

A simple, unsafe but nevertheless useful and fun ci/cd system.

## Usage

```
$ mycicd --user PSLmodels --title ParamTools --ref master 'py.test paramtools -v'
```

## Motivation

I wanted to build a tool for people I trust to run their tests on infrastructure that I maintain.

After doing some research into various types of CI/CD systems like self-hosted GitHub Actions Runners or Jenkins, I realized it was going to take a lot of effort to set them up securely. Further, it seemed like it would be just about impossible to do so securely on a public system.

So, I decided to write my own simple version to deploy on private infrastructure instead of going through the hastle of deploying a system that didn't quite do what I wanted it to anyways.
