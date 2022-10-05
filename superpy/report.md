# Technical element 1: dynamically calling a method of a class

When creating the classes the idea was to have the "CLI_router" create the correct classobject based on the "command" argument, store it as variable "obj" and then dynamically call the correct method of a class by using an argument or combination of arguments given in the CLI. Then only 1 call line would be needed instead of 1 per command. The calling code looked like this: obj.command(). F.e. if the command "buy" was inputted the classobject was made based on the Action class and the method called should be obj.buy().
Problem: the classobject was created correctly but calling the method did not work.
Solution: 
1. In the CLI_router a variable "action_wanted" is created using CLI arguments.
2. In every class a method "get_method" is added that retrieves the wanted method using the "getattr()" function, looking up the "action_wanted".
3. In the CLI_router "obj.get_method(action=action_wanted)" is called.
 ```
The code for get_method() in the classes:

class .......:
    def get_method(self, action):
        self.action = action
        method = getattr(self, self.action)
        method()
```

# Technical element 2: DRY parsing

Some parsers use the same (group of) arguments. To not have to repeat the same code several times, parent parsers are added when possible (f.e. for the parsers "buy" and "sell"). These can be found in the first part of the CLI_parser module [line 4 to 50].

# Technical element 3: userfriendly parsing

The Argparse usage and help are not very userfriendly: hard to distinguish what is optional and what is required. To make it more easy arguments are grouped and given a proper title.
For the mutually exclusive optionals this is done by adding them to an argument group => the latter excepts "title=", where the first does not.
For parent parser / main parser ".action_groups[0 or 1].title" is used to change the title of the positional or optional arguments. This is why the parsers "buy" and "sell" have multiple parent parsers: some arguments are grouped with the title "required arguments" and some are not.


