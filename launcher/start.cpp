#include <cstdlib>
#include <filesystem>
#include <iostream>

namespace fs = std::filesystem;

void install_requirements(const std::string & path) {
    std::string cmd = "\".\\bin\\python.exe\" -m pip install -r ";
    cmd += path;
    std::system(cmd.c_str());
}

int main() {
    install_requirements(".\\requirements.txt");

    // 遍历plugin目录下的所有文件
    for(auto & p: fs::recursive_directory_iterator("./plugin")) {
        if(p.path().filename() == "requirements.txt") {
            // 检查路径中是否包含"__pycache__"
            if(p.path().string().find("__pycache__") == std::string::npos) {
                install_requirements(p.path().string());
            }
        }
    }



    std::system("\".\\bin\\python.exe\" ./");
    std::system("pause");
    return 0;
}
