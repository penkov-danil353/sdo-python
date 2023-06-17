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
          	echo "Start testing process..." &&\
            echo "installing dependencies"
          """
        }
    }
    container(displayName = "PyTest", image = "ubuntu"){
      shellScript {
          content = """
          	apt update -y && apt upgrade -y && apt install -y g++ python3 python3-pip &&\
            pip install -r requirements.txt &&\
            g++ -c -o cpp_libs/parser/library.o cpp_libs/parser/library.cpp -fPIC && g++ -shared -o /usr/lib/libparse.so cpp_libs/parser/library.o &&\
            echo "run test" &&\
            cd pytests && pytest
          """
      }
    }
}
