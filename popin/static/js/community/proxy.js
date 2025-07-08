function reportBtn() {
  if (confirm("신고하시겠습니까?")) {
    alert("신고되었습니다.");
  } else {
    alert("취소");
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const modalImage = document.getElementById('modalImage');
  const imageModal = document.getElementById('imageModal');
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  const postModal = document.getElementById("postModal");
  const postList = document.querySelector(".postlist");
  const topBtn = document.getElementById('topBtn');

  const toggleBtns = document.querySelectorAll(".toggle-btn");
  const generalInput = document.getElementById("generalSearch");
  const tagInput = document.getElementById("tagSearch");
  const stateFilter = document.getElementById("stateFilter");
  const sortFilter = document.getElementById("sortFilter");
  const categoryLinks = document.querySelectorAll(".group a[data-category]");

  let imageList = [];
  let currentImageIndex = 0;

  let allCards = Array.from(document.querySelectorAll(".post-card"));
  let filteredCards = [...allCards];
  let currentPage = 1;
  const itemsPerPage = 3;

  let selectedCategory = null; // null = 전체보기

  // 이미지 모달 기능
  if (document.getElementById('modalPostImages')) {
    document.getElementById('modalPostImages').addEventListener('click', e => {
      if (e.target.tagName === 'IMG') {
        const clickedSrc = e.target.src;
        const images = Array.from(document.querySelectorAll('#modalPostImages img'));
        imageList = images.map(img => img.src);
        currentImageIndex = imageList.indexOf(clickedSrc);
        modalImage.src = clickedSrc;
        imageModal.style.display = 'flex';
      }
    });
  }

  if (imageModal) {
    imageModal.addEventListener('click', e => {
      if (e.target === modalImage) return;
      imageModal.style.display = 'none';
    });
  }

  if (prevBtn) {
    prevBtn.addEventListener('click', e => {
      e.stopPropagation();
      currentImageIndex = (currentImageIndex - 1 + imageList.length) % imageList.length;
      modalImage.src = imageList[currentImageIndex];
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', e => {
      e.stopPropagation();
      currentImageIndex = (currentImageIndex + 1) % imageList.length;
      modalImage.src = imageList[currentImageIndex];
    });
  }

  // 게시글 클릭 시 모달 열기
  if (postList) {
    postList.addEventListener("click", e => {
      const card = e.target.closest(".post-card");
      if (!card) return;

      if (e.target.closest('.report-btn') || e.target.closest('.join-btn')) return;

      const artistText = card.querySelector(".artist")?.textContent.trim() || "";
      const ptypeText = card.querySelector(".ptype")?.textContent.trim() || "";
      const title = card.querySelector(".post-title")?.textContent.trim() || "";
      const date = card.querySelector(".info-date span:nth-child(2)")?.textContent.trim() || "";
      const place = card.querySelector(".info-place span:nth-child(2)")?.textContent.trim() || "";
      const people = card.querySelector(".info-people span:nth-child(2)")?.textContent.trim() || "";
      const money = card.querySelector(".info-mon span:nth-child(2)")?.textContent.trim() || "";
      const desc = card.querySelector(".post-description")?.textContent.trim() || "";
      const wdate = card.querySelector(".post-meta")?.textContent.trim() || "";
      const imgListStr = card.getAttribute("data-imgs") || "";
      const tags = Array.from(card.querySelectorAll(".post-tag")).map(t => t.textContent.replace('#', '').trim());

      openPostModal(artistText, ptypeText, title, date, place, people, money, desc, wdate, imgListStr, tags);
    });
  }

  function openPostModal(artist, ptype, title, date, place, people, money, desc, wdate, imgStr, tags) {
    document.getElementById("modalPostArtist").textContent = artist;
    document.getElementById("modalPostPtype").textContent = ptype;
    document.getElementById("modalPostTitle").textContent = title;
    document.getElementById("modalPostDate").textContent = `📅 ${date}`;
    document.getElementById("modalPostPlace").textContent = `📍 ${place}`;
    document.getElementById("modalPostPeople").textContent = `👥 ${people}`;
    document.getElementById("modalPostMoney").textContent = `💰 ${money}`;
    document.getElementById("modalPostDescription").textContent = desc;
    document.getElementById("modalPostCreated").textContent = wdate;

    const tagContainer = document.getElementById("modalPostTags");
    tagContainer.innerHTML = "";
    if (tags.length) {
      tags.forEach(tag => {
        const span = document.createElement("span");
        span.className = "post-tag";
        span.textContent = "#" + tag;
        tagContainer.appendChild(span);
      });
      tagContainer.style.display = "flex";
      tagContainer.style.gap = "10px";
    } else {
      tagContainer.style.display = "none";
    }

    const imageContainer = document.getElementById("modalPostImages");
    imageContainer.innerHTML = "";
    if (imgStr) {
      const imgs = imgStr.split(",").map(s => s.trim());
      imageList = imgs;
      imgs.forEach(url => {
        const img = document.createElement("img");
        img.src = url;
        img.style.width = "100px";
        img.style.height = "100px";
        img.style.objectFit = "cover";
        img.style.borderRadius = "10px";
        img.style.cursor = "pointer";
        imageContainer.appendChild(img);
      });
      prevBtn.style.display = imgs.length > 1 ? 'block' : 'none';
      nextBtn.style.display = imgs.length > 1 ? 'block' : 'none';
      imageContainer.style.display = 'flex';
    } else {
      imageContainer.style.display = 'none';
    }

    postModal.style.display = "block";
    if (topBtn) {
      topBtn.style.pointerEvents = "none";
      topBtn.style.opacity = "0.4";
    }
  }

  function closePostModal() {
    postModal.style.display = "none";
    if (topBtn) {
      topBtn.style.pointerEvents = "auto";
      topBtn.style.opacity = "1";
    }
  }

  window.addEventListener("click", e => {
    if (e.target === postModal) {
      closePostModal();
    }
  });

  // TOP 버튼 동작
  if (topBtn) {
    window.addEventListener("scroll", () => {
      if (window.pageYOffset > 300) {
        topBtn.classList.add('show');
      } else {
        topBtn.classList.remove('show');
      }
    });

    topBtn.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  // 카테고리 클릭 이벤트 (href 막기)
  categoryLinks.forEach(link => {
    link.addEventListener("click", e => {
      e.preventDefault();
      selectedCategory = link.dataset.category || null;
      currentPage = 1;
      applyFilters();
    });
  });

  // 검색 모드 토글
  toggleBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      toggleBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      if (btn.dataset.type === "general") {
        generalInput.style.display = "block";
        tagInput.style.display = "none";
        tagInput.value = "";
      } else {
        generalInput.style.display = "none";
        tagInput.style.display = "block";
        generalInput.value = "";
      }
      currentPage = 1;
      applyFilters();
    });
  });

  // 검색어, 상태 필터, 정렬 필터 입력 이벤트
  [generalInput, tagInput, stateFilter, sortFilter].forEach(el => {
    if (!el) return;
    el.addEventListener("input", () => {
      currentPage = 1;
      applyFilters();
    });
  });

  // 필터/검색/정렬 적용 함수
  function applyFilters() {
    filteredCards = allCards.filter(card => {
      // 카테고리 필터
      if (selectedCategory && selectedCategory !== "전체보기" && card.dataset.category !== selectedCategory) {
        return false;
      }

      // 검색 필터
      const searchType = document.querySelector(".toggle-btn.active")?.dataset.type || "general";
      const keyword = (searchType === "general" ? generalInput.value : tagInput.value).toLowerCase().trim();

      if (keyword) {
        if (searchType === "general") {
          const title = card.querySelector(".post-title")?.textContent.toLowerCase() || "";
          const artist = card.querySelector(".artist")?.textContent.toLowerCase() || "";
          if (!title.includes(keyword) && !artist.includes(keyword)) {
            return false;
          }
        } else {
          const tags = Array.from(card.querySelectorAll(".post-tag")).map(t => t.textContent.toLowerCase().replace('#', '').trim());
          if (!tags.some(t => t.includes(keyword))) return false;
        }
      }

      // 상태 필터
      const selectedState = stateFilter.value;
      if (selectedState && selectedState !== "" && card.querySelector(".post-status")?.textContent !== selectedState) {
        return false;
      }
      currentPage = Math.min(currentPage, Math.ceil(filteredCards.length / itemsPerPage) || 1);
      applyPagination();

      return true;
    });

    // 정렬 필터
    const sortValue = sortFilter.value;
    if (sortValue === "최신순") {
      filteredCards.sort((a, b) => {
        const dateA = new Date(a.querySelector(".post-meta")?.textContent || 0);
        const dateB = new Date(b.querySelector(".post-meta")?.textContent || 0);
        return dateB - dateA;
      });
    } else if (sortValue === "조회순") {
      filteredCards.sort((a, b) => {
        const viewsA = parseInt(a.querySelector(".participants span:first-child")?.textContent.replace("👁️", "").trim()) || 0;
        const viewsB = parseInt(b.querySelector(".participants span:first-child")?.textContent.replace("👁️", "").trim()) || 0;
        return viewsB - viewsA;
      });
    }

    // 해당게시글없다 문구
      const noResults = document.getElementById("noResultsMessage");
        if (filteredCards.length === 0) {
          noResults.style.display = "block";
        } else {
          noResults.style.display = "none";
        }

    currentPage = Math.min(currentPage, Math.ceil(filteredCards.length / itemsPerPage) || 1);
    applyPagination();
  }

  // 페이지네이션 적용 함수
  function applyPagination() {
  allCards.forEach(card => card.style.display = "none");

  const totalPages = Math.ceil(filteredCards.length / itemsPerPage) || 1;
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const pageCards = filteredCards.slice(startIndex, endIndex);

  pageCards.forEach(card => card.style.display = "block");

  updatePaginationUI(totalPages);  // <-- 페이지네이션 UI 갱신

  window.scrollTo({ top: 0, behavior: "smooth" });
}

  function updatePaginationUI(totalPages) {
    const pagination = document.querySelector(".pagination");
    if (!pagination) return;

    pagination.innerHTML = "";

    const createPageLink = (text, page, disabled = false, active = false) => {
      const a = document.createElement("a");
      a.href = "#";
      a.textContent = text;
      if (disabled) a.classList.add("disabled");
      if (active) a.classList.add("active");
      a.addEventListener("click", e => {
        e.preventDefault();
        if (disabled || active) return;
        currentPage = page;
        applyPagination();
      });
      return a;
    };

    pagination.appendChild(createPageLink("«", 1, currentPage === 1));
    pagination.appendChild(createPageLink("‹", currentPage - 1, currentPage === 1));

    let startPage = Math.max(1, currentPage - 2);
    let endPage = Math.min(totalPages, startPage + 4);
    if (endPage - startPage < 4) {
      startPage = Math.max(1, endPage - 4);
    }

    for (let i = startPage; i <= endPage; i++) {
      pagination.appendChild(createPageLink(i, i, false, currentPage === i));
    }

    pagination.appendChild(createPageLink("›", currentPage + 1, currentPage === totalPages));
    pagination.appendChild(createPageLink("»", totalPages, currentPage === totalPages));
  }

  // 초기 필터 적용
  applyFilters();

  // 모달 닫기 버튼 연결
  document.querySelector(".close-btn").addEventListener("click", closePostModal);
});
