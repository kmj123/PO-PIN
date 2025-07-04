// 신고 함수
function reportBtn(){
if(confirm("신고하시겠습니까?")){
    alert("신고되었습니다.");
}else{
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
const topBtn = document.getElementById('topBtn');
const regionFilter = document.getElementById('regionFilter');
const sortFilter = document.getElementById('sortFilter');

// 이미지 썸네일 클릭 시 이미지 확대 모달 띄우기
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

// 이미지 확대 모달 닫기 (이미지 클릭은 닫히지 않음)
imageModal.addEventListener('click', (e) => {
if (e.target === modalImage) return;
imageModal.style.display = 'none';
});

// 이전 이미지 보기
prevBtn.addEventListener('click', (e) => {
e.stopPropagation();
currentImageIndex = (currentImageIndex - 1 + imageList.length) % imageList.length;
modalImage.src = imageList[currentImageIndex];
});

// 다음 이미지 보기
nextBtn.addEventListener('click', (e) => {
e.stopPropagation();
currentImageIndex = (currentImageIndex + 1) % imageList.length;
modalImage.src = imageList[currentImageIndex];
});

// 모달 열기 (매개변수 순서 맞춤)
function openPostModal(artistText, ptypeText, title, date, place, desc, imgListStr = "", tags = []) {

const artistEl = document.getElementById("modalPostArtist");
const ptypeEl = document.getElementById("modalPostPtype");

artistEl.textContent = artistText;
artistEl.className = "artist";

ptypeEl.textContent = ptypeText;
typeEl.className = "ptype";

document.getElementById("modalPostTitle").textContent = title;
document.getElementById("modalPostDate").textContent = `📅 ${date}`;
document.getElementById("modalPostPlace").textContent = `📍 ${place}`;
document.getElementById("modalPostDescription").textContent = desc;

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
    imageContainer.appendChild(img);
    });

    prevBtn.style.display = imgUrls.length > 1 ? 'block' : 'none';
    nextBtn.style.display = imgUrls.length > 1 ? 'block' : 'none';
    imageContainer.style.display = 'flex';
} else {
    imageContainer.style.display = 'none';
}

postModal.style.display = "block";

// topBtn 비활성화
topBtn.style.pointerEvents = 'none';
topBtn.style.opacity = '0.4';
}

// 모달 닫기
function closePostModal() {
postModal.style.display = "none";

// topBtn 활성화
topBtn.style.pointerEvents = 'auto';
topBtn.style.opacity = '1';
}

// 모달 바깥 클릭 시 닫기
window.onclick = function(event) {
if (event.target === postModal) {
    closePostModal();
}
}

document.querySelectorAll(".post-card").forEach(card => {
card.addEventListener("click", (event) => {
    // 신고 버튼, 참여 버튼 등 클릭 시 모달 열기 막기
    if (
    event.target.closest('.report-btn') || 
    event.target.closest('.join-btn') || 
    event.target.closest('.post-actions')
    ) {
    return;
    }

    const artistText = card.querySelector(".artist")?.textContent.trim();
    const ptypeText = card.querySelector(".ptype")?.textContent.trim();
    const title = card.querySelector(".post-title")?.textContent.trim();
    const date = card.querySelector(".info-date span:nth-child(2)")?.textContent.trim();
    const place = card.querySelector(".info-place span:nth-child(2)")?.textContent.trim();
    const desc = card.querySelector(".post-description")?.textContent.trim();
    const imgListStr = card.getAttribute("data-imgs") || "";
    const tags = Array.from(card.querySelectorAll(".post-tag")).map(tag => tag.textContent.replace('#', '').trim());

    openPostModal(artistText, ptypeText, title, date, place, desc, imgListStr, tags);
});
});

// Top 버튼 기능
window.addEventListener('scroll', function () {
if (window.pageYOffset > 300) {
    topBtn.classList.add('show');
} else {
    topBtn.classList.remove('show');
}
});

topBtn.addEventListener('click', function () {
window.scrollTo({
    top: 0,
    behavior: 'smooth'
});
});

// 지역 + 최신순 필터링
if (regionFilter && sortFilter) {
regionFilter.addEventListener("change", applyFilters);
sortFilter.addEventListener("change", applyFilters);
}

function applyFilters() {
const selectedRegion = regionFilter.value;
const sortOrder = sortFilter.value;
const postCards = Array.from(document.querySelectorAll(".post-card"));

let filtered = postCards;
if (selectedRegion !== "") {
    filtered = filtered.filter(card => {
    const region = card.querySelector(".ptype")?.textContent.trim().toLowerCase() || "";
    return region === selectedRegion.toLowerCase();
    });
}

filtered.sort((a, b) => {
    const dateA = new Date(a.querySelector(".info-date span:nth-child(2)")?.textContent.trim());
    const dateB = new Date(b.querySelector(".info-date span:nth-child(2)")?.textContent.trim());
    return sortOrder === "latest" ? dateB - dateA : dateA - dateB;
});

postCards.forEach(card => card.style.display = "none");
filtered.forEach(card => card.style.display = "block");
}
