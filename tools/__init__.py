import subprocess
import os
from typing import Optional
from config.settings import settings


class GitTool:
    def __init__(self):
        self.enabled = settings.ENABLE_GIT_TOOL

    def run_command(self, command: str, cwd: str = None) -> str:
        if not self.enabled:
            return "Git 工具未启用"
        try:
            result = subprocess.run(
                command,
                cwd=cwd or settings.PROJECT_ROOT,
                shell=True,
                capture_output=True,
                text=True,
                timeout=settings.TOOL_EXECUTION_TIMEOUT
            )
            return result.stdout or result.stderr
        except Exception as e:
            return str(e)

    def clone_repo(self, repo_url: str, target_dir: str = None) -> str:
        return self.run_command(f"git clone {repo_url} {target_dir or ''}")

    def commit(self, message: str) -> str:
        return self.run_command(f"git commit -m \"{message}\"")

    def push(self, branch: str = "main") -> str:
        return self.run_command(f"git push origin {branch}")

    def pull(self, branch: str = "main") -> str:
        return self.run_command(f"git pull origin {branch}")

    def status(self) -> str:
        return self.run_command("git status")

    def log(self, limit: int = 10) -> str:
        return self.run_command(f"git log --oneline -n {limit}")


class DockerTool:
    def __init__(self):
        self.enabled = settings.ENABLE_DOCKER_TOOL

    def run_command(self, command: str) -> str:
        if not self.enabled:
            return "Docker 工具未启用"
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=settings.TOOL_EXECUTION_TIMEOUT
            )
            return result.stdout or result.stderr
        except Exception as e:
            return str(e)

    def build(self, dockerfile: str = "Dockerfile", tag: str = None) -> str:
        tag_arg = f"-t {tag}" if tag else ""
        return self.run_command(f"docker build {tag_arg} -f {dockerfile} .")

    def run(self, image: str, command: str = None, ports: str = None) -> str:
        port_arg = f"-p {ports}" if ports else ""
        cmd_arg = f"-- {command}" if command else ""
        return self.run_command(f"docker run {port_arg} {image} {cmd_arg}")

    def ps(self) -> str:
        return self.run_command("docker ps")

    def images(self) -> str:
        return self.run_command("docker images")

    def stop(self, container_id: str) -> str:
        return self.run_command(f"docker stop {container_id}")

    def rm(self, container_id: str) -> str:
        return self.run_command(f"docker rm {container_id}")


class CICDTool:
    def __init__(self):
        self.enabled = settings.ENABLE_CICD_TOOL

    def run_command(self, command: str) -> str:
        if not self.enabled:
            return "CI/CD 工具未启用"
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=settings.TOOL_EXECUTION_TIMEOUT
            )
            return result.stdout or result.stderr
        except Exception as e:
            return str(e)

    def run_tests(self, test_command: str = "python -m pytest") -> str:
        return self.run_command(test_command)

    def lint(self, lint_command: str = "python -m flake8") -> str:
        return self.run_command(lint_command)

    def build(self, build_command: str = "python setup.py build") -> str:
        return self.run_command(build_command)

    def deploy(self, deploy_command: str) -> str:
        return self.run_command(deploy_command)
