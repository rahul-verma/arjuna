# Arjuna API Reference

## Classes

### Configuration

#### Properties
- `name`: Name of configuration
- `builder` - Returns a `ConfigBuilder` object to create custom configurations. The builder uses this `Configuration` object's option values as reference.

#### Methods
- `value(<Arjuna Option or string>)`: Retrive value of configuration option represented as `ArjunaOption` enum constant or a string representing the option. The option name string is considered by Arjuna as **case-insensitive**. Also, **. (dot)** and **_ (underscore)** are interchangeable. So, following are equivalent arguments:
    - ArjunaOption.BROWSER_NAME
    - BROWSER_NAME
    - BrOwSeR_NaMe
    - browser.name
    - Browser.Name
    - and so on

#### Special Operators
The `Configuration` object also allows for retrieval of a config option using the `. (dot notation)` or `[name] i.e. (dict-like name based retrieval)`.

### ConfigBuilder

#### Methods
- `option(key, value)`: Add an option.
- `from_file(name_or_path`): Load configuration options from a file path. If instead of full absolute path, a name or relative file path is provided, Arjuna creates the path in relation to the default configuration directory - `<Project Root>/config`.
- `register(name)`: Creates and returns a configuration by super-imposing its options on top of the `Configuration` object's values associated with it. If `name` is not provided, a dynamic name is generated.

#### Special Operators
The `ConfigBuiler` object allows `. dot notation` or `[] dict style` for adding/updating options.

