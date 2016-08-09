# ninja-modifier
 Copyright (C) 2016 Skymizer. All Rights Reserved.

 You may not use this file except in compliance with the License.


 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 
 Author: asmailada
 
 Last update time: 2016/08/01

 ### Introduction

 It is a tool for ninja build system that modified *.ninja files.
 Allow user to add any cflags for specific source file.
 Using python.

First, you need a json file to indicate the relation between target source files and a  set of cflags as below:
		
```sh		
test.json
			{
			    "src": {
			        "SOURCES": {
			            "ninja.cc": "-Ofast -marm -finline-limit=501",
			            "build.cc": "-Ofast -marm -finline-limit=502"
			        }
			    }
			}
```
### Running Ninja-Modifier

1. Before running Ninja-Modifier while building Chromium Project, notice that you need to run 

`
	gn gen out/Default target
`

to make sure everything is up-to-date.


2. Run Ninja-Modifier 

`
	python ninja_modifier.py -C chromium/src/ -in test.json
`

`-C`	The working directory for Ninja-Modifier to scan all *.ninja files. This will make a changing for working directory to chromium/src/

`-in`	The input json file. Ninja-Modifier will read this file after changing working directory. Therefore, the file path needed to be relative to -C path.


### Flow
		1. Ninja-Modifier first changing the working directory to `-C` argument.
		2. Read in json file.
		3. Traverse CWD to find all `*.ninja` files and cache the rules, build settings.
		4. According to the description in json file, create specific rules and rewrite the build settings for each source file.

### Notice

**Before using this tool, please run `gn gen out/Default` to checkout all files.**

Due to the machenism of ninja build system in building Chromium OS, running `ninja` will make an automatically update of all *.ninja files while source files had changes, which will cause a rewrite of all *.ninja files if we use this tool without first checkout all files.


### Problems
		1.  More effecient addRule() should be implement. (skip unchange *.ninja files)
		2.  Need to come up with a more organized style.
