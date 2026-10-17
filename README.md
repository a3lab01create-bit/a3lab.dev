# a3lab.dev

a3lab 회사 소개 사이트 https://a3lab.dev 의 원본과 배포 파일입니다.
GitHub Pages가 `main` 브랜치의 `docs/` 폴더를 그대로 배포합니다.

## 구조

| 경로 | 내용 |
|---|---|
| `index.html` | 페이지 원본. Claude 아티팩트 형식이라 `<head>`가 없습니다. |
| `brand/og.html` | 링크 미리보기 이미지(1200×630) 원본 |
| `brand/icon.html` | 아이콘(512×512) 원본 |
| `build.py` | 원본으로 `docs/`를 만드는 스크립트 |
| `docs/` | 실제로 배포되는 사이트. 직접 고치지 말고 `build.py`로 다시 만듭니다. |

## 수정하고 배포하기

1. `index.html`을 고칩니다.
2. `docs/`를 다시 만듭니다.
   ```bash
   python3 build.py
   ```
   미리보기 이미지나 아이콘까지 다시 만들 때는 `python3 build.py --images`를 씁니다.
   macOS의 Google Chrome과 Pillow(`pip install pillow`)가 필요합니다.
3. 커밋하고 `main`에 push하면 1분 안에 a3lab.dev에 반영됩니다.

## 도메인

- a3lab.dev는 Cloudflare에서 등록했고 DNS도 Cloudflare에서 관리합니다.
- A 레코드 4개(`185.199.108.153` ~ `185.199.111.153`)와 `www` CNAME(`a3lab01create-bit.github.io`) 모두 프록시 없이(DNS only) 둡니다.
- HTTPS 인증서는 GitHub Pages가 자동으로 발급하고 갱신합니다.
