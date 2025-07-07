// 신고
function reportBtn() {
    if (confirm("신고하시겠습니까?")) {
        alert("신고되었습니다.");
    } else {
        alert("취소");
    }
}

const postModal = document.getElementById("postModal");
const modalImage = document.getElementById('modalImage');
const imageModal = document.getElementById('imageModal');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const topBtn = document.getElementById('topBtn');
const sortSelect = document.getElementById('sortSelect'); // HTML의 <select id="sortSelect">와 일치

let currentImageIndex = 0;
let imageList = [];
let currentPage = 1;
const postsPerPage = 6;

// 이미지 썸네일 클릭 시 모달 띄우기
document.getElementById('modalPostImages').addEventListener('click', (e) => {
    if (e.target.tagName === 'IMG') {
        const clickedSrc = e.target.src;
        const images = Array.from(document.querySelectorAll('#modalPostImages img'));
        imageList = images.map(img => img.src);
        currentImageIndex = imageList.indexOf(clickedSrc);
        modalImage.src = clickedSrc;
        imageModal.style.display = 'flex';
    }
});

// 이미지 모달 닫기
imageModal.addEventListener('click', (e) => {
    // 모달 이미지 자체가 아닌 배경 클릭 시 닫히도록
    if (e.target === modalImage) return; // 이미지 클릭 시에는 닫지 않음
    imageModal.style.display = 'none';
});

// 이미지 이전/다음
prevBtn.addEventListener('click', (e) => {
    e.stopPropagation(); // 이벤트 버블링 방지 (모달 닫힘 방지)
    currentImageIndex = (currentImageIndex - 1 + imageList.length) % imageList.length;
    modalImage.src = imageList[currentImageIndex];
});

nextBtn.addEventListener('click', (e) => {
    e.stopPropagation(); // 이벤트 버블링 방지 (모달 닫힘 방지)
    currentImageIndex = (currentImageIndex + 1) % imageList.length;
    modalImage.src = imageList[currentImageIndex];
});

// 모달 열기
function openPostModal(artistText, stypeText, title, date, place, check, desc, imgListStr = "", tags = [], wdate = "") {
    document.getElementById("modalPostArtist").textContent = artistText;
    document.getElementById("modalPostStype").textContent = stypeText;
    document.getElementById("modalPostTitle").textContent = title;
    document.getElementById("modalPostDate").textContent = `📅 ${date}`;
    document.getElementById("modalPostPlace").textContent = `📍 ${place}`;
    document.getElementById("modalPostCheck").textContent = `✅ ${check}`;
    document.getElementById("modalPostDescription").textContent = desc;
    document.getElementById("modalPostCreated").textContent = `작성일: ${wdate}`; // 작성일 표시

    const tagsContainer = document.getElementById("modalPostTags");
    tagsContainer.innerHTML = ""; // 기존 태그 비우기
    if (tags.length > 0) {
        tags.forEach(tag => {
            const span = document.createElement("span");
            span.className = "post-tag";
            span.textContent = `#${tag}`;
            tagsContainer.appendChild(span);
        });
        tagsContainer.style.display = "flex";
        tagsContainer.style.gap = "10px";
    } else {
        tagsContainer.style.display = "none"; // 태그가 없으면 숨김
    }

    const imageContainer = document.getElementById("modalPostImages");
    imageContainer.innerHTML = ""; // 기존 이미지 비우기
    if (imgListStr) {
        const imgUrls = imgListStr.split(",").map(url => url.trim());
        imageList = imgUrls; // 현재 모달의 이미지 목록 업데이트
        imgUrls.forEach(url => {
            const img = document.createElement("img");
            img.src = url;
            img.alt = "첨부 이미지";
            img.style.width = "100px";
            img.style.height = "100px";
            img.style.objectFit = "cover";
            img.style.borderRadius = "10px";
            imageContainer.appendChild(img);
        });

        // 이미지가 1개 초과일 때만 이전/다음 버튼 표시
        prevBtn.style.display = imgUrls.length > 1 ? 'block' : 'none';
        nextBtn.style.display = imgUrls.length > 1 ? 'block' : 'none';
        imageContainer.style.display = 'flex';
    } else {
        imageContainer.style.display = 'none'; // 이미지가 없으면 숨김
        prevBtn.style.display = 'none'; // 이미지 없을 땐 버튼도 숨김
        nextBtn.style.display = 'none';
    }

    postModal.style.display = "block"; // 게시글 상세 모달 표시
    topBtn.style.pointerEvents = 'none'; // Top 버튼 비활성화
    topBtn.style.opacity = '0.4';
}

function closePostModal() {
    postModal.style.display = "none"; // 게시글 상세 모달 숨김
    topBtn.style.pointerEvents = 'auto'; // Top 버튼 활성화
    topBtn.style.opacity = '1';
}

// 모달 외부 클릭 시 닫기
window.onclick = function (event) {
    if (event.target === postModal) {
        closePostModal();
    }
}

function setupPostCardEvents() {
    document.querySelectorAll(".post-card").forEach(card => {
        card.addEventListener("click", (event) => {
            // 버튼이나 특정 액션 영역 클릭 시 모달 열지 않음
            if (
                event.target.tagName === 'BUTTON' ||
                event.target.closest('.post-actions') ||
                event.target.closest('.report-btn') ||
                event.target.closest('.join-btn')
            ) return;

            // post-card에서 정보 추출
            const artistText = card.querySelector(".artist")?.textContent.trim();
            const stypeText = card.querySelector(".stype")?.textContent.trim();
            const title = card.querySelector(".post-title")?.textContent.trim();
            const date = card.querySelector(".info-date span:nth-child(2)")?.textContent.trim();
            const place = card.querySelector(".info-place span:nth-child(2)")?.textContent.trim();
            const check = card.querySelector(".info-check span:nth-child(2)")?.textContent.trim();
            const desc = card.querySelector(".post-description")?.textContent.trim();
            const imgListStr = card.getAttribute("data-imgs") || ""; // data-imgs 속성에서 이미지 URL 가져오기
            const tags = Array.from(card.querySelectorAll(".post-tag")).map(tag => tag.textContent.replace('#', '').trim());
            const wdate = card.querySelector(".post-meta")?.textContent.trim(); // 작성일 정보 가져오기

            openPostModal(artistText, stypeText, title, date, place, check, desc, imgListStr, tags, wdate);
        });
    });
}

setupPostCardEvents(); // 페이지 로드 시 게시글 카드 이벤트 설정

// Top 버튼
window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
        topBtn.classList.add('show');
    } else {
        topBtn.classList.remove('show');
    }
});

topBtn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// 정렬 셀렉트 박스 변경 시 필터 적용
if (sortSelect) {
    sortSelect.addEventListener('change', applyFilters);
}

// 페이지네이션 생성 및 렌더링
function renderPagination(totalPosts, perPage) {
    const paginationContainer = document.querySelector('.pagination');
    if (!paginationContainer) return;

    const totalPages = Math.ceil(totalPosts / perPage);
    paginationContainer.innerHTML = ""; // 기존 페이지네이션 버튼 비우기

    // 첫 페이지 버튼 "«"
    const firstPageBtn = document.createElement('button');
    firstPageBtn.textContent = '«';
    firstPageBtn.addEventListener('click', () => {
        if (currentPage !== 1) {
            currentPage = 1;
            applyFilters();
        }
    });
    paginationContainer.appendChild(firstPageBtn);

    // 이전 페이지 버튼 "‹"
    const prevPageBtn = document.createElement('button');
    prevPageBtn.textContent = '‹';
    prevPageBtn.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            applyFilters();
        }
    });
    paginationContainer.appendChild(prevPageBtn);

    // 페이지 번호 버튼들
    for (let i = 1; i <= totalPages; i++) {
        const btn = document.createElement('button');
        btn.textContent = i;
        btn.className = (i === currentPage) ? 'active' : ''; // 현재 페이지 활성화
        btn.addEventListener('click', () => {
            currentPage = i;
            applyFilters();
        });
        paginationContainer.appendChild(btn);
    }

    // 다음 페이지 버튼 "›"
    const nextPageBtn = document.createElement('button');
    nextPageBtn.textContent = '›';
    nextPageBtn.addEventListener('click', () => {
        if (currentPage < totalPages) {
            currentPage++;
            applyFilters();
        }
    });
    paginationContainer.appendChild(nextPageBtn);

    // 마지막 페이지 버튼 "»"
    const lastPageBtn = document.createElement('button');
    lastPageBtn.textContent = '»';
    lastPageBtn.addEventListener('click', () => {
        if (currentPage !== totalPages) {
            currentPage = totalPages;
            applyFilters();
        }
    });
    paginationContainer.appendChild(lastPageBtn);
}

// 검색, 필터, 정렬, 페이지네이션을 통합하여 적용하는 함수
window.addEventListener('DOMContentLoaded', () => {
    const generalInput = document.getElementById("generalSearch");
    const tagInput = document.getElementById("tagSearch");
    const stateFilter = document.getElementById("stateFilter"); // HTML의 <select id="stateFilter">와 일치
    const toggleBtns = document.querySelectorAll(".toggle-btn");

    // 검색 타입 토글 버튼 이벤트
    toggleBtns.forEach(btn => {
        btn.addEventListener("click", function () {
            toggleBtns.forEach(b => b.classList.remove("active"));
            this.classList.add("active");

            if (this.dataset.type === "general") {
                generalInput.style.display = "block";
                tagInput.style.display = "none";
                tagInput.value = ""; // 태그 검색창 초기화
            } else {
                generalInput.style.display = "none";
                tagInput.style.display = "block";
                generalInput.value = ""; // 일반 검색창 초기화
            }
            currentPage = 1; // 검색 타입 변경 시 1페이지로 리셋
            applyFilters();
        });
    });

    // 검색 입력 및 필터/정렬 변경 시 이벤트 리스너
    [generalInput, tagInput, stateFilter, sortSelect].forEach(input => {
        if (input) {
            if (input.tagName === 'SELECT') {
                input.addEventListener("change", () => {
                    currentPage = 1; // 필터/정렬 변경 시 1페이지로 리셋
                    applyFilters();
                });
            } else { // input[type="text"]
                input.addEventListener("input", () => {
                    currentPage = 1; // 검색어 입력 시 1페이지로 리셋
                    applyFilters();
                });
            }
        }
    });

    // 필터링 및 정렬 로직을 실제로 수행하는 함수
    window.applyFilters = function () {
        const searchType = document.querySelector(".toggle-btn.active")?.dataset.type || "general";
        const keyword = (searchType === "general" ? generalInput?.value : tagInput?.value || "").toLowerCase().trim();
        const selectedState = stateFilter?.value; // "나눔 종류" 필터 값
        const sortOption = sortSelect?.value || "";

        let cards = Array.from(document.querySelectorAll(".post-card"));
        // 모든 카드를 일단 보이게 설정 (필터링 전)
        cards.forEach(card => card.style.display = "block");

        // 필터링 로직
        cards = cards.filter(card => {
            let showCard = true;

            // 검색어 필터
            if (keyword) {
                if (searchType === "general") {
                    const title = card.querySelector(".post-title")?.textContent.toLowerCase() || "";
                    const artist = card.querySelector(".artist")?.textContent.toLowerCase() || "";
                    const description = card.querySelector(".post-description")?.textContent.toLowerCase() || "";
                    showCard = title.includes(keyword) || artist.includes(keyword) || description.includes(keyword);
                } else { // 태그 검색
                    const tags = Array.from(card.querySelectorAll(".post-tag")).map(tag => tag.textContent.toLowerCase().replace('#', '').trim());
                    showCard = tags.some(tag => tag.includes(keyword));
                }
            }

            // "나눔 종류" 필터 (stateFilter)
            // 'stype' 클래스를 가진 요소의 텍스트가 selectedState와 일치하는지 확인
            if (showCard && selectedState && selectedState !== "" && selectedState !== "전체") {
                const postStype = card.querySelector(".stype")?.textContent.trim() || "";
                showCard = postStype === selectedState;
            }

            // 만약 'regionFilter'와 같은 다른 필터가 있다면 여기에 추가
            // if (showCard && selectedRegion && selectedRegion !== "") {
            //   const region = card.querySelector(".region")?.textContent.toLowerCase().replace(/\s+/g, '') || "";
            //   const selected = selectedRegion.toLowerCase().replace(/\s+/g, '');
            //   showCard = region.includes(selected) || selected.includes(region);
            // }

            return showCard;
        });

        // 정렬 로직
        if (sortOption === "latest") { // 최신순
            cards.sort((a, b) => {
                const dateA = new Date(a.querySelector(".post-meta")?.textContent);
                const dateB = new Date(b.querySelector(".post-meta")?.textContent);
                return dateB - dateA; // 최신 날짜가 앞으로
            });
        } else if (sortOption === "popular") { // 조회순
            cards.sort((a, b) => {
                // .participants span에서 숫자만 추출 (예: "👁️ 67" -> 67)
                const viewsA = parseInt(a.querySelector(".participants span")?.textContent.replace(/[^\d]/g, "")) || 0;
                const viewsB = parseInt(b.querySelector(".participants span")?.textContent.replace(/[^\d]/g, "")) || 0;
                return viewsB - viewsA; // 조회수가 높은 것이 앞으로
            });
        }

        const postList = document.querySelector(".postlist");
        if (postList) {
            postList.innerHTML = ""; // 게시글 목록 비우기

            const totalPosts = cards.length;
            const start = (currentPage - 1) * postsPerPage;
            const end = start + postsPerPage;
            const paginatedCards = cards.slice(start, end); // 현재 페이지에 해당하는 게시글만 가져옴

            if (paginatedCards.length === 0) {
                // 검색 결과가 없을 때 메시지 표시
                const noPostsMessage = document.createElement("p");
                noPostsMessage.textContent = "검색 결과가 없습니다.";
                noPostsMessage.style.textAlign = "center";
                noPostsMessage.style.marginTop = "20px";
                noPostsMessage.style.fontSize = "1.2em";
                noPostsMessage.style.color = "#888";
                postList.appendChild(noPostsMessage);
            } else {
                // 필터링/정렬된 게시글을 다시 추가
                paginatedCards.forEach(card => postList.appendChild(card));
            }
            renderPagination(totalPosts, postsPerPage); // 페이지네이션 업데이트
        }

        setupPostCardEvents(); // 새로 렌더링된 카드에 이벤트 리스너 다시 연결
    }

    applyFilters(); // 페이지 로드 시 초기 필터 적용 (모든 게시글 표시)
});