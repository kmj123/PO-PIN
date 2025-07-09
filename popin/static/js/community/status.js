// 신고
function reportBtn(){
  alert("신고");
}

// 모달
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
function openPostModal(artistText, regionText, ptypeText, title, date, place, desc, imgListStr = "", tags = [], wdate = "") {

const artistEl = document.getElementById("modalPostArtist");
const ptypeEl = document.getElementById("modalPostPtype");
const regionEl = document.getElementById("modalPostRegion");

artistEl.textContent = artistText;
artistEl.className = "artist";

ptypeEl.textContent = ptypeText;
ptypeEl.className = "ptype";

regionEl.textContent = regionText;
regionEl.className = "region";

document.getElementById("modalPostTitle").textContent = title;
document.getElementById("modalPostDate").textContent = `📅 ${date}`;
document.getElementById("modalPostPlace").textContent = `📍 ${place}`;
document.getElementById("modalPostDescription").textContent = desc;
document.getElementById("modalPostCreated").textContent = wdate;

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
    const regionText = card.querySelector(".region")?.textContent.trim();
    const ptypeText = card.querySelector(".ptype")?.textContent.trim();
    const title = card.querySelector(".post-title")?.textContent.trim();
    const date = card.querySelector(".info-date span:nth-child(2)")?.textContent.trim();
    const place = card.querySelector(".info-place span:nth-child(2)")?.textContent.trim();
    const wdate = card.querySelector(".post-meta")?.textContent.trim();
    const desc = card.querySelector(".post-description")?.textContent.trim();
    const imgListStr = card.getAttribute("data-imgs") || "";
    const tags = Array.from(card.querySelectorAll(".post-tag")).map(tag => tag.textContent.replace('#', '').trim());

    openPostModal(artistText, regionText, ptypeText, title, date, place, desc, imgListStr, tags, wdate);
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


// 페이지네이션
const allCards = Array.from(document.querySelectorAll(".post-card"));
let filteredCards = [...allCards];
let currentPage = 1;
let itemsPerPage = 3;

// 페이지네이션 메인 함수
function showPage(pageNumber) {
  currentPage = pageNumber;
  hideAllCards();
  showCurrentPageCards();
  updatePageButtons();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function hideAllCards() {
  allCards.forEach(card => {
    card.style.display = "none";
  });
}

function showCurrentPageCards() {
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const cardsToShow = filteredCards.slice(startIndex, endIndex);

  cardsToShow.forEach(card => {
    card.style.display = "block";
  });
}

function updatePageButtons() {
  const pagination = document.querySelector(".pagination");
  if (!pagination) return;

  const totalPages = Math.ceil(filteredCards.length / itemsPerPage);
  pagination.innerHTML = "";

  if (totalPages <= 1) return;

  const navButtons = createNavigationButtons(totalPages);
  pagination.appendChild(navButtons.firstBtn);
  pagination.appendChild(navButtons.prevBtn);

  createPageNumberButtons(pagination, totalPages);

  pagination.appendChild(navButtons.nextBtn);
  pagination.appendChild(navButtons.lastBtn);
}

function createNavigationButtons(totalPages) {
  const firstBtn = createButton("«", "첫 페이지", () => {
    if (currentPage > 1) showPage(1);
  });

  const prevBtn = createButton("‹", "이전 페이지", () => {
    if (currentPage > 1) showPage(currentPage - 1);
  });

  const nextBtn = createButton("›", "다음 페이지", () => {
    if (currentPage < totalPages) showPage(currentPage + 1);
  });

  const lastBtn = createButton("»", "마지막 페이지", () => {
    if (currentPage < totalPages) showPage(totalPages);
  });

  if (currentPage === 1) {
    firstBtn.classList.add('disabled');
    prevBtn.classList.add('disabled');
  }

  if (currentPage === totalPages) {
    nextBtn.classList.add('disabled');
    lastBtn.classList.add('disabled');
  }

  return { firstBtn, prevBtn, nextBtn, lastBtn };
}

function createPageNumberButtons(pagination, totalPages) {
  const maxVisiblePages = 5;
  let startPage, endPage;

  if (totalPages <= maxVisiblePages) {
    startPage = 1;
    endPage = totalPages;
  } else {
    startPage = Math.max(1, currentPage - 2);
    endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);
    if (endPage === totalPages) {
      startPage = Math.max(1, endPage - maxVisiblePages + 1);
    }
  }

  for (let i = startPage; i <= endPage; i++) {
    const pageBtn = createPageButton(i, i === currentPage);
    pagination.appendChild(pageBtn);
  }
}

function createButton(text, title, clickHandler) {
  const button = document.createElement("a");
  button.href = "#";
  button.title = title;
  button.textContent = text;
  button.addEventListener("click", (e) => {
    e.preventDefault();
    if (!button.classList.contains('disabled')) {
      clickHandler();
    }
  });
  return button;
}

function createPageButton(pageNumber, isCurrentPage) {
  if (isCurrentPage) {
    const currentBtn = document.createElement("strong");
    currentBtn.textContent = pageNumber;
    currentBtn.classList.add('current-page');
    return currentBtn;
  } else {
    return createButton(pageNumber, `${pageNumber}페이지`, () => {
      showPage(pageNumber);
    });
  }
}

function resetPagination(newFilteredCards) {
  filteredCards = newFilteredCards;
  currentPage = 1;
  showPage(1);
}

function initializePagination() {
  filteredCards = Array.from(document.querySelectorAll(".post-card"));
  showPage(1);
}

document.addEventListener("DOMContentLoaded", initializePagination);


document.addEventListener("DOMContentLoaded", () => {
  const generalInput = document.getElementById("generalSearch");
  const tagInput = document.getElementById("tagSearch");
  const regionFilter = document.getElementById("regionFilter");
  const sortFilter = document.getElementById("sortFilter");
  const toggleBtns = document.querySelectorAll(".toggle-btn");
  
  let searchMode = "general";

  toggleBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      toggleBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      searchMode = btn.dataset.type;
      if (searchMode === "general") {
        generalInput.style.display = "inline-block";
        tagInput.style.display = "none";
      } else {
        generalInput.style.display = "none";
        tagInput.style.display = "inline-block";
      }
      applyFilters();
    });
  });


  // 입력, 필터 변경 이벤트
  generalInput.addEventListener("input", applyFilters);
  tagInput.addEventListener("input", applyFilters);
  regionFilter.addEventListener("change", applyFilters);
  sortFilter.addEventListener("change", applyFilters);

   function applyFilters() {
    const keyword = (searchMode === "general" ? generalInput.value : tagInput.value).toLowerCase();
    const selectedRegion = regionFilter.value;
    const sortBy = sortFilter.value;

    filteredCards = allCards.filter(card => {
      const title = card.querySelector(".post-title")?.textContent.toLowerCase() || "";
      const region = card.querySelector(".region")?.textContent || "";
      const tags = Array.from(card.querySelectorAll(".post-tag")).map(t => t.textContent.toLowerCase());

      let matchesSearch = true;
      if (keyword) {
        matchesSearch = searchMode === "general"
          ? title.includes(keyword)
          : tags.some(tag => tag.includes(keyword));
      }

      let matchesRegion = !selectedRegion || selectedRegion === "" || region === selectedRegion;

      return matchesSearch && matchesRegion;
    });

    if (sortBy === "최신순") {
        filteredCards.sort((a, b) => {
          const dateA = new Date(a.querySelector(".post-meta")?.dataset.date || "1970-01-01");
          const dateB = new Date(b.querySelector(".post-meta")?.dataset.date || "1970-01-01");
          return dateB - dateA; // 최신순 내림차순
        });
      } else if (sortBy === "조회순") {
        filteredCards.sort((a, b) => {
          const viewsAtext = a.querySelector(".participants span")?.textContent || "0";
          const viewsBtext = b.querySelector(".participants span")?.textContent || "0";

          const viewsA = parseInt(viewsAtext.replace(/[^\d]/g, ""), 10) || 0;
          const viewsB = parseInt(viewsBtext.replace(/[^\d]/g, ""), 10) || 0;

          return viewsB - viewsA; // 조회순 내림차순
        });
      }
      
      console.log("정렬 후 filteredCards 날짜:", filteredCards.map(card => card.querySelector(".post-meta").dataset.date));
      console.log("정렬 후 filteredCards 조회수:", filteredCards.map(card => card.querySelector(".participants span").textContent));

        resetPagination(filteredCards);
      }


  // 초기 실행
  applyFilters();
});
