### Gui Namespace - Externalizing Identifiers

After launching a `WebApp`, apart from basic browser operations, most of times an automated test finds and interacts with Gui elements.

Externalizing of identifiers is built into Arjuna and is a MUST to do UI automation with Arjuna. The object which contains identification information and related meta-data of a Gui is referred to as `GuiNamespace (GNS)` in Arjuna.

#### The GNS File

Arjuna uses YAML as the format for externalization of identifiers. Fow now, we will discuss basic usage of the format.

Location for the following file is `arjuna-samples/arjex_app/guiauto/namespace/BasicIdentification.yaml`

```YAML
labels:

  user_id:
    id: user_login

  user_name:
    name: log

  user_tag:
    tag: input

  user_class:
    classes: input

  lost_pass_link:
    link: password

  lost_pass_flink:
    flink: "Lost your password?"
```

##### Points to note
1. This file has a `YAML` extension.
2. All labels are placed under `labels` heading.
3. Each label represents element identification information which can be later referenced by this label.
3. The label should be a valid Arjuna name.
4. In its basic usage format, the section has a key value pair for a given locator type. For example `id: user_login`.
5. Labels are treated as **case-insensitive** by Arjuna.

We'll use this YAML file in the next section.