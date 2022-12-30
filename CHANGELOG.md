# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2022-12-30

### Changed

- Fixed typos in logging
- Creation of database and scheme as well as insertion of the KG data was
moved to a special class called `AutoLoadableSQLiteKG`. The `SQLiteKG` isn't
handling this anymore. It only expects a URI for the database connection,
and expects the database to represent the KG already.

### Fixed

 - Issue [#1](https://github.com/khaller93/sqlitekg2vec/issues/1): SQLite KG was
changed into a lightweight class such that it can be pickled properly for
multiprocessing.