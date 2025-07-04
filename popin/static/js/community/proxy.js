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
const topBtn = document.getElementById('topBtn');

// 페이지네이션 관련 변수 추가
let currentPage = 1;
let itemsPerPage = 2; // 페이지당 게시글 수
let totalItems = 0;
let filteredCards = [];

// 이미지 썸네일 클릭 시 모달
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

// 모달 열기
function openPostModal(artistText, ptypeText, title, date, place, people, money, desc, imgListStr = "", tags = [], wdate = "") {
  const artistEl = document.getElementById("modalPostArtist");
  const ptypeEl = document.getElementById("modalPostPtype");

  artistEl.textContent = artistText;
  artistEl.className = "artist";

  ptypeEl.textContent = ptypeText;
  ptypeEl.className = "ptype";

  document.getElementById("modalPostTitle").textContent = title;
  document.getElementById("modalPostDate").textContent = `📅 ${date}`;
  document.getElementById("modalPostPlace").textContent = `📍 ${place}`;
  document.getElementById("modalPostPeople").textContent = `👥 ${people}`;
  document.getElementById("modalPostMoney").textContent = `💰 ${money}`;
  document.getElementById("modalPostDescription").textContent = desc;
  document.getElementById("modalPostCreated").textContent = wdate; // 날짜 설정

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
  topBtn.style.pointerEvents = 'none';
  topBtn.style.opacity = '0.4';
}

function closePostModal() {
  postModal.style.display = "none";
  topBtn.style.pointerEvents = 'auto';
  topBtn.style.opacity = '1';
}

window.onclick = function (event) {
  if (event.target === postModal) {
    closePostModal();
  }
}

// 카드 클릭
document.querySelectorAll(".post-card").forEach(card => {
  card.addEventListener("click", (event) => {
    if (
      event.target.closest('.report-btn') || 
      event.target.closest('.join-btn') || 
      event.target.closest('.post-actions')
    ) return;

    const artistText = card.querySelector(".artist")?.textContent.trim();
    const ptypeText = card.querySelector(".ptype")?.textContent.trim();
    const title = card.querySelector(".post-title")?.textContent.trim();
    const date = card.querySelector(".info-date span:nth-child(2)")?.textContent.trim();
    const place = card.querySelector(".info-place span:nth-child(2)")?.textContent.trim();
    const people = card.querySelector(".info-people span:nth-child(2)")?.textContent.trim();
    const money = card.querySelector(".info-mon span:nth-child(2)")?.textContent.trim();
    const desc = card.querySelector(".post-description")?.textContent.trim();
    const wdate = card.querySelector(".post-meta")?.textContent.trim(); // 날짜 추가
    const imgListStr = card.getAttribute("data-imgs") || "";
    const tags = Array.from(card.querySelectorAll(".post-tag")).map(tag => tag.textContent.replace('#', '').trim());

    openPostModal(artistText, ptypeText, title, date, place, people, money, desc, imgListStr, tags, wdate);
  });
});

// Top 버튼
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

// 검색/필터/정렬/페이지네이션 기능
document.addEventListener("DOMContentLoaded", function () {
  const toggleBtns = document.querySelectorAll(".toggle-btn");
  const generalInput = document.getElementById("generalSearch");
  const tagInput = document.getElementById("tagSearch");
  const regionFilter = document.getElementById("regionFilter");
  const stateFilter = document.getElementById("stateFilter");
  const sortFilter = document.getElementById("sortFilter");

  toggleBtns.forEach(btn => {
    btn.addEventListener("click", function () {
      toggleBtns.forEach(b => b.classList.remove("active"));
      this.classList.add("active");

      const type = this.dataset.type;
      if (type === "general") {
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

  if (generalInput) generalInput.addEventListener("input", applyFilters);
  if (tagInput) tagInput.addEventListener("input", applyFilters);
  if (regionFilter) regionFilter.addEventListener("change", applyFilters);
  if (stateFilter) stateFilter.addEventListener("change", applyFilters);
  if (sortFilter) sortFilter.addEventListener("change", applyFilters);

  function applyFilters() {
    const searchType = document.querySelector(".toggle-btn.active")?.dataset.type || "general";
    const keyword = (searchType === "general" ? generalInput?.value : tagInput?.value || "").toLowerCase().trim();
    const selectedRegion = regionFilter?.value;
    const selectedState = stateFilter?.value;
    const selectedSort = sortFilter?.value;

    const postCards = document.querySelectorAll(".post-card");
    let visibleCards = [];

    postCards.forEach(card => {
      let showCard = true;

      if (keyword) {
        if (searchType === "general") {
          const title = card.querySelector(".post-title")?.textContent.toLowerCase() || "";
          const artist = card.querySelector(".artist")?.textContent.toLowerCase() || "";
          const desc = card.querySelector(".post-description")?.textContent.toLowerCase() || "";
          showCard = title.includes(keyword) || artist.includes(keyword) || desc.includes(keyword);
        } else {
          const tags = Array.from(card.querySelectorAll(".post-tag")).map(tag =>
            tag.textContent.toLowerCase().replace('#', '').trim()
          );
          showCard = tags.some(tag => tag.includes(keyword));
        }
      }

      if (showCard && selectedRegion && selectedRegion !== "") {
        const region = card.querySelector(".ptype")?.textContent.trim().toLowerCase() || "";
        showCard = region.includes(selectedRegion.toLowerCase());
      }

      if (showCard && selectedState && selectedState !== "") {
        const state = card.querySelector(".post-status")?.textContent.trim().toLowerCase() || "";
        showCard = state === selectedState.toLowerCase();
      }

      if (showCard) {
        visibleCards.push(card);
      }
    });

    // 현재 페이지를 1로 리셋
    currentPage = 1;

    // 정렬 기능 적용
    if (selectedSort && selectedSort !== "") {
      applySorting(visibleCards, selectedSort);
    } else {
      filteredCards = visibleCards;
      applyPagination();
    }
  }

  function applySorting(cards, sortType) {
    // 날짜 파싱 함수
    function parseDate(dateString) {
      const parts = dateString.split('-');
      if (parts.length === 3) {
        return new Date(parts[0], parts[1] - 1, parts[2]);
      }
      return new Date();
    }

    // 조회수 파싱 함수
    function parseViews(viewString) {
      const match = viewString.match(/(\d+)/);
      return match ? parseInt(match[1]) : 0;
    }

    // 카드 정렬
    cards.sort((a, b) => {
      if (sortType === "최신순") {
        const dateA = parseDate(a.querySelector(".post-meta")?.textContent.trim() || "");
        const dateB = parseDate(b.querySelector(".post-meta")?.textContent.trim() || "");
        return dateB - dateA; // 최신순 (내림차순)
      } else if (sortType === "조회순") {
        const viewsA = parseViews(a.querySelector(".participants span:first-child")?.textContent.trim() || "");
        const viewsB = parseViews(b.querySelector(".participants span:first-child")?.textContent.trim() || "");
        return viewsB - viewsA; // 조회수 높은 순 (내림차순)
      }
      return 0;
    });

    // 정렬된 카드들을 전역 변수에 저장
    filteredCards = cards;
    
    // 페이지네이션 적용
    applyPagination();
  }

  // 페이지네이션 함수
  function applyPagination() {
    const container = document.querySelector(".postlist");
    const allCards = document.querySelectorAll(".post-card");
    
    // 모든 카드 숨기기
    allCards.forEach(card => {
      card.style.display = "none";
    });

    // 총 아이템 수 업데이트
    totalItems = filteredCards.length;
    
    // 현재 페이지에 표시할 카드들 계산
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const cardsToShow = filteredCards.slice(startIndex, endIndex);

    // 현재 페이지 카드들만 표시하고 올바른 순서로 배치
    cardsToShow.forEach((card, index) => {
      card.style.display = "block";
      // 페이지네이션 요소 바로 앞에 삽입
      const pagination = container.querySelector(".pagination");
      container.insertBefore(card, pagination);
    });

    // 페이지네이션 UI 업데이트
    updatePaginationUI();
  }

  // 페이지네이션 UI 업데이트 함수
  function updatePaginationUI() {
    const pagination = document.querySelector(".pagination");
    if (!pagination) return;

    const totalPages = Math.ceil(totalItems / itemsPerPage);
    
    // 기존 페이지네이션 내용 제거
    pagination.innerHTML = "";

    // 첫 페이지 버튼
    const firstBtn = document.createElement("a");
    firstBtn.href = "#";
    firstBtn.title = "첫 페이지";
    firstBtn.textContent = "«";
    firstBtn.addEventListener("click", (e) => {
      e.preventDefault();
      if (currentPage > 1) {
        currentPage = 1;
        applyPagination();
      }
    });
    pagination.appendChild(firstBtn);

    // 이전 페이지 버튼
    const prevBtn = document.createElement("a");
    prevBtn.href = "#";
    prevBtn.title = "이전 페이지";
    prevBtn.textContent = "‹";
    prevBtn.addEventListener("click", (e) => {
      e.preventDefault();
      if (currentPage > 1) {
        currentPage--;
        applyPagination();
      }
    });
    pagination.appendChild(prevBtn);

    // 페이지 번호 버튼들
    const startPage = Math.max(1, currentPage - 2);
    const endPage = Math.min(totalPages, currentPage + 2);

    for (let i = startPage; i <= endPage; i++) {
      const pageBtn = document.createElement(i === currentPage ? "strong" : "a");
      pageBtn.textContent = i;
      
      if (i === currentPage) {
        // 현재 페이지는 strong 태그
        pagination.appendChild(pageBtn);
      } else {
        // 다른 페이지는 링크
        pageBtn.href = "#";
        pageBtn.addEventListener("click", (e) => {
          e.preventDefault();
          currentPage = i;
          applyPagination();
        });
        pagination.appendChild(pageBtn);
      }
    }

    // 다음 페이지 버튼
    const nextBtn = document.createElement("a");
    nextBtn.href = "#";
    nextBtn.title = "다음 페이지";
    nextBtn.textContent = "›";
    nextBtn.addEventListener("click", (e) => {
      e.preventDefault();
      if (currentPage < totalPages) {
        currentPage++;
        applyPagination();
      }
    });
    pagination.appendChild(nextBtn);

    // 마지막 페이지 버튼
    const lastBtn = document.createElement("a");
    lastBtn.href = "#";
    lastBtn.title = "마지막 페이지";
    lastBtn.textContent = "»";
    lastBtn.addEventListener("click", (e) => {
      e.preventDefault();
      if (currentPage < totalPages) {
        currentPage = totalPages;
        applyPagination();
      }
    });
    pagination.appendChild(lastBtn);
  }

  // 초기 로드 시 모든 카드를 filteredCards에 설정
  filteredCards = Array.from(document.querySelectorAll(".post-card"));
  applyPagination();
});