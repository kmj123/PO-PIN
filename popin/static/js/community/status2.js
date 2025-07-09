document.addEventListener("DOMContentLoaded", function () {

  const modalImage = document.getElementById('modalImage');
  const imageModal = document.getElementById('imageModal');
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  const postModal = document.getElementById("postModal");
  const topBtn = document.getElementById("topBtn");

  let currentImageIndex = 0;
  let imageList = [];

  // 후기 카드 클릭 시 모달 열기
  document.querySelectorAll(".post-item").forEach(item => {
    item.addEventListener("click", (e) => {
      if (
            e.target.closest('.report-btn') || 
            e.target.closest('.join-btn') || 
            e.target.closest('.post-actions')
    ) {
    return;
    }

    const artistText = item.querySelector(".artist")?.textContent.trim();
    const regionText = item.querySelector(".region")?.textContent.trim();
    const ptypeText = item.querySelector(".ptype")?.textContent.trim();
    const title = item.querySelector(".post-title")?.textContent.trim();
    const date = item.querySelector(".info-date span:nth-child(2)")?.textContent.trim();
    const place = item.querySelector(".info-place span:nth-child(2)")?.textContent.trim();
    const desc = item.querySelector(".post-description")?.textContent.trim();
    const imgListStr = item.getAttribute("data-imgs") || "";
    const tags = Array.from(item.querySelectorAll(".post-tag")).map(tag => tag.textContent.replace('#', '').trim());

    openPostModal(artistText, regionText, ptypeText, title, date, place, desc, imgListStr, tags);
    });
  });

    // 모달 열기
    function openPostModal(artistText, regionText, ptypeText, title, date, place, desc, imgListStr = "", tags = []) {

    const artistEl = document.getElementById("modalPostArtist");
    const regionEl = document.getElementById("modalPostRegion");
    const ptypeEl = document.getElementById("modalPostPtype");

    artistEl.textContent = artistText;
    artistEl.className = "artist";

    regionEl.textContent = regionText;
    regionEl.className = "region";

    ptypeEl.textContent = ptypeText;
    ptypeEl.className = "ptype";

    document.getElementById("modalPostTitle").textContent = title;
    document.getElementById("modalPostDate").textContent = `📅 ${date}`;
    document.getElementById("modalPostPlace").textContent = `📍 ${place}`;
    document.getElementById("modalPostDescription").textContent = desc;

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

    if (imageUrls.length > 0 && imageUrls[0] !== "") {
      imageList = imageUrls.map(url => url.trim());
      imageList.forEach(url => {
        const img = document.createElement("img");
        img.src = url;
        img.alt = "후기 이미지";
        img.style.width = "100px";
        img.style.height = "100px";
        img.style.objectFit = "cover";
        img.style.borderRadius = "10px";
        imageContainer.appendChild(img);
      });

      imageContainer.style.display = "flex";

      if (imageList.length > 1) {
        prevBtn.style.display = 'block';
        nextBtn.style.display = 'block';
      } else {
        prevBtn.style.display = 'none';
        nextBtn.style.display = 'none';
      }
    } else {
      imageContainer.style.display = "none";
      prevBtn.style.display = 'none';
      nextBtn.style.display = 'none';
    }

    postModal.style.display = "flex";
    topBtn.style.pointerEvents = 'none';
    topBtn.style.opacity = '0.4';
  }

  // 모달 닫기
  window.closePostModal = function () {
    postModal.style.display = "none";
    topBtn.style.pointerEvents = 'auto';
    topBtn.style.opacity = '1';
  }

  // 바깥 클릭 시 닫기
  window.addEventListener("click", function (event) {
    if (event.target === postModal) {
      closePostModal();
    }
  });

  // 이미지 썸네일 클릭 시 전체보기
  const imageContainer = document.getElementById('modalPostImages');
  if (imageContainer) {
    imageContainer.addEventListener('click', (e) => {
      if (e.target.tagName === 'IMG') {
        const clickedSrc = e.target.src;
        const images = Array.from(imageContainer.querySelectorAll('img'));
        imageList = images.map(img => img.src);
        currentImageIndex = imageList.indexOf(clickedSrc);
        modalImage.src = clickedSrc;
        imageModal.style.display = 'flex';
      }
    });
  }

  if (imageModal) {
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
  }

  // Top 버튼 기능
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

  // 검색 및 필터링 기능
  const generalInput = document.getElementById("generalSearch");
  const tagInput = document.getElementById("tagSearch");
  const regionFilter = document.getElementById("regionFilter");
  const sortFilter = document.getElementById("sortSelect");
  const toggleBtns = document.querySelectorAll(".toggle-btn");
  const postitems = Array.from(document.querySelectorAll(".post-item"));

  // 토글 버튼 클릭 시 검색 입력창 전환
  toggleBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      toggleBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      const type = btn.dataset.type;
      if (type === "general") {
        generalInput.style.display = "inline-block";
        tagInput.style.display = "none";
      } else {
        generalInput.style.display = "none";
        tagInput.style.display = "inline-block";
      }
      applyFilters();
    });
  });

  // 검색 입력 이벤트
  generalInput.addEventListener("input", applyFilters);
  tagInput.addEventListener("input", applyFilters);
  regionFilter.addEventListener("change", applyFilters);
  sortFilter.addEventListener("change", applyFilters);

  // 검색/필터/정렬 적용 함수
  function applyFilters() {
    const searchMode = document.querySelector(".toggle-btn.active")?.dataset.type || "general";
    const keyword = (searchMode === "general" ? generalInput.value : tagInput.value).toLowerCase();
    const selectedRegion = regionFilter.value;
    const sortBy = sortFilter.value;

    let filtered = postItems.filter(item => {
      const title = item.querySelector(".post-title")?.textContent.toLowerCase() || "";
      const tags = Array.from(item.querySelectorAll(".post-tag")).map(tag => tag.textContent.toLowerCase());
      const region = card.querySelector(".region")?.textContent.trim().toLowerCase() || "";

      // 검색 필터
      let matchSearch = true;
      if (keyword) {
        if (searchMode === "general") {
          matchSearch = title.includes(keyword) || writer.includes(keyword) || partner.includes(keyword);
        } else {
          matchSearch = tags.some(tag => tag.includes(keyword));
        }
      }

      // 지역 필터
      let matchRegion = true;
      if (matchRegion && selectedRegion && selectedRegion !== "") {
        matchRegion = region === selectedRegion;
      }

      return matchSearch && matchRegion;
    });

    // 정렬
    if (sortBy) {
      filtered.sort((a, b) => {
        if (sortBy === "latest") {
          const dateA = new Date(a.querySelector(".post-date")?.textContent.trim() || 0);
          const dateB = new Date(b.querySelector(".post-date")?.textContent.trim() || 0);
          return dateB - dateA;
        } else if (sortBy === "views") {
          const viewsA = parseInt(a.querySelector(".post-meta span:last-child")?.textContent.replace("👁️", "").trim() || 0);
          const viewsB = parseInt(b.querySelector(".post-meta span:last-child")?.textContent.replace("👁️", "").trim() || 0);
          return viewsB - viewsA;
        }
        return 0;
      });
    }

    // 페이지네이션 초기화 및 적용
    resetPagination(filtered);
  }

  // 초기 필터링 적용
  applyFilters();
});