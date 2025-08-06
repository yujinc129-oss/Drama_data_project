# 이 셀을 그대로 복사해서 사용하세요.

def git_push(file_path):
    """
    지정한 파일을 GitHub의 정해진 위치('data/processed/')에 업로드합니다.
    이 함수는 오직 파일 경로 하나만 인자로 받습니다.
    """
    # --- 함수 내부에 필요한 모든 라이브러리 import ---
    # 이 함수만 복사하면 되도록 모든 import를 안에 넣었습니다.
    import os
    from google.colab import userdata
    from github import Github, GithubException

    # --- 모든 설정값이 함수 내부에 고정되어 있습니다 ---
    GITHUB_USERNAME = "yujinc129-oss"
    REPO_NAME = "Drama_data_project"
    DESTINATION_FOLDER = "data/processed" # 항상 이 폴더에 저장됩니다.
    # ----------------------------------------------------

    # 1. 파일 이름 추출 및 GitHub에 저장될 최종 경로 설정
    file_name = os.path.basename(file_path)
    github_path = f"{DESTINATION_FOLDER}/{file_name}"

    # 2. GitHub 인증 및 API 객체 생성
    try:
        GITHUB_TOKEN = userdata.get('GITHUB_TOKEN')
        g = Github(GITHUB_TOKEN)
        repo = g.get_user(GITHUB_USERNAME).get_repo(REPO_NAME)
    except Exception as e:
        print(f"🚨 GitHub 인증 또는 저장소 연결에 실패했습니다: {e}")
        return

    # 3. 로컬 파일 읽기
    try:
        with open(file_path, 'rb') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"🚨 Colab에서 '{file_path}' 파일을 찾을 수 없습니다.")
        return

    # 4. GitHub에 파일 업로드 (있으면 업데이트, 없으면 생성)
    try:
        # 파일이 이미 있는지 확인
        contents = repo.get_contents(github_path)
        # 있으면 업데이트
        repo.update_file(
            path=contents.path,
            message=f"Update: {file_name}",
            content=content,
            sha=contents.sha
        )
        print(f"✅ 파일 업데이트 성공: '{github_path}'")

    except GithubException as e:
        if e.status == 404:
            # 파일이 없으면 새로 생성
            repo.create_file(
                path=github_path,
                message=f"Create: {file_name}",
                content=content
            )
            print(f"✅ 파일 업로드 성공: '{github_path}'")
        else:
            # 그 외 GitHub 오류
            print(f"🚨 GitHub 작업 중 오류가 발생했습니다: {e}")
    except Exception as e:
        print(f"🚨 예기치 못한 오류가 발생했습니다: {e}")


