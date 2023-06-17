/**
* JetBrains Space Automation
* This Kotlin script file lets you automate build activities
* For more info, see https://www.jetbrains.com/help/space/automation.html
*/

job("test") {
  	startOn {
        gitPush {
            anyBranchMatching {
                +"*/dev"
            }
        }
    }
    host("Run echo") {
    	shellScript {
          content = """
          	echo "Start testing process..."
          """
        }
    }
    host("Run echo") {
    	shellScript {
          content = """
          	echo "installing dependencies"
          """
        }
    }
    container(displayName = "PyTest", image = "python3.10"){
      shellScript {
          content = """
          	apt update -y && apt upgrade -y && apt install -y g++
          """
      }
      shellScript {
          content = """
          	pip install -r requirements.txt
          """
      }
      shellScript {
          content = """
          	g++ -c -o cpp_libs/parser/library.o cpp_libs/parser/library.cpp -fPIC && g++ -shared -o cpp_libs/parser/libparse.so cpp_libs/parser/library.o
          """
      }
      shellScript {
          content = """
          	mv cpp_libs/parser/libparse.so /usr/lib
          """
      }
      shellScript {
          content = """
          	echo "run test"
          """
      }
      shellScript {
          content = """
          	cd pytests && pytest
          """
      }
    }
}
