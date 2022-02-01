
# KonFu

## Origin Story
There comes a time in every daemon's life when if needs to know what to do.
Normally, this may come from a direct command from a higher power, but
more typically involves a configuration file. Configuration files come in
many formats, shapes and sizes but editing them is always a pain.

Most GUIs are defined by tediously setting up form elements with validation
rules, and then build/bake/test (aka "yell loudly because the damned
element did not render correctly after four hours playing with it even though
I did everything right (even tried reading the manual)
and it's not my fault and WTH is THAT doing here?").

A standard called `JSON-schema` exists which attempts to extract the
name/type/validation part of this mess out of the way, and provides a way
to externally validate a file against the schema defintion. Nice!

Even better, there is a `React JS` JavaScript library that will take a
JSON schema file and create the form for us! Now we're talking!

Now all we need is a container that take schema files and configuration files,
feed them into the ECMA monster spaghetti-hell (aka JavaScript), and then 
we never need to write a form handler using Python Flask again.

This magical image shall contain all of the Configuration Fu (Kon Fu)
that we need in order to attain configuration file mastery of mind and body.

## Form 1: `Waddling Panda`

Our first step in our journey of configuration enlightmennt is our baby
steps, and seeing what's in the box:

    make run

This should build the Docker image and then start the container.

Unless you don't have Docker set up and configured.

Also, you might need to download the base image.


