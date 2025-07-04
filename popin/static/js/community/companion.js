// 신고
function reportBtn() {
if (confirm("신고하시겠습니까?")) {
    alert("신고되었습니다.");
} else {
    alert("취소");
}
}

const modalImage = document.getElementById('modalImage');
let currentImageIndex = 0;
let imageList = [];

const imageModal = document.getElementById('imageModal');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const postModal = document.getElementById("postModal");

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

imageModal.addEventListener('click', (e) => {
if (e.target === modalImage) return;
imageModal.style.display = 'none';
});

prevBtn.addEventListener('click', (e) => {
e.stopPropagation();
currentImageIndex = (currentImageIndex - 1 + imageList.length) % imageList.length;
modalImage.src = imageList[currentImageIndex];
});

nextBtn.addEventListener('click', (e) => {
e.stopPropagation();
currentImageIndex = (currentImageIndex + 1) % imageList.length;
modalImage.src = imageList[currentImageIndex];
});

// 게시글 카드 클릭 이벤트
document.querySelector(".postlist").addEventListener("click", (e) => {
const card = e.target.closest(".post-card");
if (!card) return;

// 클릭한 게 신고 버튼이나 참여 버튼이면 모달 열지 않음
if (
    e.target.closest('.report-btn') ||
    e.target.closest('.join-btn')
) return;

const artistText = card.querySelector(".artist")?.textContent.trim();
const regionText = card.querySelector(".region")?.textContent.trim();
const title = card.querySelector(".post-title")?.textContent.trim();
const date = card.querySelector(".info-date span:nth-child(2)")?.textContent.trim();
const place = card.querySelector(".info-place span:nth-child(2)")?.textContent.trim();
const people = card.querySelector(".info-people span:nth-child(2)")?.textContent.trim();
const desc = card.querySelector(".post-description")?.textContent.trim();
const wdate = card.querySelector(".post-meta")?.textContent.trim(); // 날짜 추가
const imgListStr = card.getAttribute("data-imgs") || "";
const tags = Array.from(card.querySelectorAll(".post-tag")).map(tag => tag.textContent.replace('#', '').trim());

openPostModal(artistText, regionText, title, date, place, people, desc, imgListStr, tags, wdate);
});

// 모달 열기
function openPostModal(artistText, regionText, title, date, place, people, desc, imgListStr = "", tags = [], wdate = "") {
const artistEl = document.getElementById("modalPostArtist");
const regionEl = document.getElementById("modalPostRegion");

artistEl.textContent = artistText;
artistEl.className = "artist";

regionEl.textContent = regionText;
regionEl.className = "region";

document.getElementById("modalPostTitle").textContent = title;
document.getElementById("modalPostDate").textContent = `📅 ${date}`;
document.getElementById("modalPostPlace").textContent = `📍 ${place}`;
document.getElementById("modalPostPeople").textContent = `👥 ${people}`;
document.getElementById("modalPostDescription").textContent = desc;
document.getElementById("modalPostCreated").textContent = wdate; // 날짜 설정

// 태그 출력
const tagsContainer = document.getElementById("modalPostTags");
tagsContainer.innerHTML = "";
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
    tagsContainer.style.display = "none";
}

// 이미지 출력
const imageContainer = document.getElementById("modalPostImages");
imageContainer.innerHTML = "";
if (imgListStr) {
    const imgUrls = imgListStr.split(",").map(url => url.trim());
    imageList = imgUrls;

    imgUrls.forEach(url => {
    const img = document.createElement("img");
    img.src = url;
    img.alt = "첨부 이미지";
    img.style.width = "100px";
    img.style.height = "100px";
    img.style.objectFit = "cover";
    img.style.borderRadius = "10px";
    img.style.cursor = "pointer";
    imageContainer.appendChild(img);
    });

    prevBtn.style.display = imgUrls.length > 1 ? 'block' : 'none';
    nextBtn.style.display = imgUrls.length > 1 ? 'block' : 'none';
    imageContainer.style.display = 'flex';
} else {
    imageContainer.style.display = 'none';
}

postModal.style.display = "block";

// Top 버튼 비활성화
const topBtn = document.getElementById('topBtn');
if (topBtn) {
    topBtn.style.pointerEvents = 'none';
    topBtn.style.opacity = '0.4';
}
}

function closePostModal() {
postModal.style.display = "none";
const topBtn = document.getElementById('topBtn');
if (topBtn) {
    topBtn.style.pointerEvents = 'auto';
    topBtn.style.opacity = '1';
}
}

// 바깥 클릭 시 닫기
window.onclick = function (event) {
if (event.target === postModal) {
    closePostModal();
}
}

// Top 버튼 기능
const topBtn = document.getElementById('topBtn');
if (topBtn) {
window.addEventListener('scroll', function () {
    if (window.pageYOffset > 300) {
    topBtn.classList.add('show');
    } else {
    topBtn.classList.remove('show');
    }
});

topBtn.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});
}

// 검색 토글 기능
document.addEventListener("DOMContentLoaded", function () {
const toggleBtns = document.querySelectorAll(".toggle-btn");
const generalInput = document.getElementById("generalSearch");
const tagInput = document.getElementById("tagSearch");
const regionFilter = document.getElementById("regionFilter");
const stateFilter = document.getElementById("stateFilter");

// 검색 모드 토글
toggleBtns.forEach(btn => {
    btn.addEventListener("click", function() {
    toggleBtns.forEach(b => b.classList.remove("active"));
    this.classList.add("active");
    
    const searchType = this.dataset.type;
    if (searchType === "general") {
        generalInput.style.display = "block";
        tagInput.style.display = "none";
        tagInput.value = "";
    } else {
        generalInput.style.display = "none";
        tagInput.style.display = "block";
        generalInput.value = "";
    }
    applyFilters();
    });
});

// 검색/필터 이벤트 바인딩
if (generalInput) generalInput.addEventListener("input", applyFilters);
if (tagInput) tagInput.addEventListener("input", applyFilters);
if (regionFilter) regionFilter.addEventListener("change", applyFilters);
if (stateFilter) stateFilter.addEventListener("change", applyFilters);

function applyFilters() {
    const searchMode = document.querySelector(".toggle-btn.active")?.dataset.type || "general";
    const keyword = (searchMode === "general" ? generalInput?.value : tagInput?.value || "").toLowerCase().trim();
    const selectedRegion = regionFilter?.value;
    const selectedState = stateFilter?.value;

    const postCards = document.querySelectorAll(".post-card");
    
    postCards.forEach(card => {
    let showCard = true;

    // 검색 필터
    if (keyword) {
        if (searchMode === "general") {
        const title = card.querySelector(".post-title")?.textContent.toLowerCase() || "";
        const artist = card.querySelector(".artist")?.textContent.toLowerCase() || "";
        showCard = title.includes(keyword) || artist.includes(keyword);
        } else {
        const tags = Array.from(card.querySelectorAll(".post-tag")).map(tag => 
            tag.textContent.toLowerCase().replace('#', '').trim()
        );
        showCard = tags.some(tag => tag.includes(keyword));
        }
    }

    // 지역 필터 (수정된 부분)
    if (showCard && selectedRegion && selectedRegion !== "") {
        const region = card.querySelector(".region")?.textContent.trim().toLowerCase() || "";
        showCard = region.includes(selectedRegion.toLowerCase());
        }

    // 상태 필터
    if (showCard && selectedState && selectedState !== "") {
        const state = card.querySelector(".post-status")?.textContent.trim() || "";
        showCard = state === selectedState;
    }

    // 카드 표시/숨김
    card.style.display = showCard ? "block" : "none";
    });
}
});