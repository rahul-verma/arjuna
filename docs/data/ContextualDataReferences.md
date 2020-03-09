### Contextual Data References and the Magic `R` Function

There are various situations in which you need contextual data. Such a need is catered by the concept of Contextual Data References (or simply Data References) in Arjuna.

Consider the following example:
1. You have 3 types of user accounts - `Bronze`, `Silver` and `Gold`.
2. The user account information includes a `User` and `Pwd` to repesented user name and password representing a given account type.
3. In different situations, you want to use the user accounts and retrieve them by the context name from a single source of information.

Arjuna supports Excel based data references out of the box. These reference files are automatically loaded when `Arjuna.init()` is called by Arjuna launcher.
