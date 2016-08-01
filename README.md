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

 # Description
 It is a tool for ninja build system that modified *.ninja files to append cflags on source files which user concerned.

You first need a json file to describe the target source files as below:
		
```sh		
test.json
			{
				"../../cc/layers": {
			        "SOURCES": {
			            "video_layer.cc": "-O3 -O3 -O3"				        
			        }
			    }
			}
```

### Usage

Default:

`
python ninja_modifier.py -in test.json
`

Specifying a directory to work on:

`
python ninja_modifier.py -in test.json -C path/you/want
`

### Flow
		1.  Read in json file
		2.  Traverse the specific directory(or cwd) and its subdirectory to find all *.ninja files
		3.  Inside *.ninja files, find current building rules as reference and add new rules according to the description in the json file.

### Problems
		1.  More effecient addRule() should be implement. (skip unchange *.ninja files)
		2.  Need to come up with a more organized style.
