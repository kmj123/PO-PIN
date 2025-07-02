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

let currentImageIndex = 0;
let imageList = [];

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
  if (e.target === modalImage) return;
  imageModal.style.display = 'none';
});

// 이미지 이전/다음
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
function openPostModal(artistText, stypeText, title, date, place, check, desc, imgListStr = "", tags = []) {
  document.getElementById("modalPostArtist").textContent = artistText;
  document.getElementById("modalPostStype").textContent = stypeText;
  document.getElementById("modalPostTitle").textContent = title;
  document.getElementById("modalPostDate").textContent = `📅 ${date}`;
  document.getElementById("modalPostPlace").textContent = `📍 ${place}`;
  document.getElementById("modalPostCheck").textContent = `✅ ${check}`;
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

// 후기 카드 클릭
document.querySelectorAll(".post-card").forEach(card => {
  card.addEventListener("click", (event) => {
    if (
      event.target.tagName === 'BUTTON' ||
      event.target.closest('.post-actions') ||
      event.target.closest('.report-btn') ||
      event.target.closest('.join-btn')
    ) return;

    const artistText = card.querySelector(".artist")?.textContent.trim();
    const stypeText = card.querySelector(".stype")?.textContent.trim();
    const title = card.querySelector(".post-title")?.textContent.trim();
    const date = card.querySelector(".info-date span:nth-child(2)")?.textContent.trim();
    const place = card.querySelector(".info-place span:nth-child(2)")?.textContent.trim();
    const check = card.querySelector(".info-check span:nth-child(2)")?.textContent.trim();
    const desc = card.querySelector(".post-description")?.textContent.trim();
    const imgListStr = card.getAttribute("data-imgs") || "";
    const tags = Array.from(card.querySelectorAll(".post-tag")).map(tag => tag.textContent.replace('#', '').trim());

    openPostModal(artistText, stypeText, title, date, place, check, desc, imgListStr, tags);
  });
});

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

// 검색 및 필터
document.addEventListener("DOMContentLoaded", function () {
  const generalInput = document.getElementById("generalSearch");
  const tagInput = document.getElementById("tagSearch");
  const regionFilter = document.getElementById("regionFilter");
  const stateFilter = document.getElementById("stateFilter");
  const toggleBtns = document.querySelectorAll(".toggle-btn");

  toggleBtns.forEach(btn => {
    btn.addEventListener("click", function () {
      toggleBtns.forEach(b => b.classList.remove("active"));
      this.classList.add("active");

      if (this.dataset.type === "general") {
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

  [generalInput, tagInput, regionFilter, stateFilter].forEach(input => {
    if (input) input.addEventListener("input", applyFilters);
    if (input?.tagName === 'SELECT') input.addEventListener("change", applyFilters);
  });

  function applyFilters() {
    const searchType = document.querySelector(".toggle-btn.active")?.dataset.type || "general";
    const keyword = (searchType === "general" ? generalInput?.value : tagInput?.value || "").toLowerCase().trim();
    const selectedRegion = regionFilter?.value;
    const selectedState = stateFilter?.value;

    document.querySelectorAll(".post-card").forEach(card => {
      let showCard = true;

      if (keyword) {
        if (searchType === "general") {
          const title = card.querySelector(".post-title")?.textContent.toLowerCase() || "";
          const artist = card.querySelector(".artist")?.textContent.toLowerCase() || "";
          showCard = title.includes(keyword) || artist.includes(keyword);
        } else {
          const tags = Array.from(card.querySelectorAll(".post-tag")).map(tag => tag.textContent.toLowerCase().replace('#', '').trim());
          showCard = tags.some(tag => tag.includes(keyword));
        }
      }

      if (showCard && selectedRegion && selectedRegion !== "") {
        const region = card.querySelector(".stype")?.textContent.toLowerCase().replace(/\s+/g, '') || "";
        const selected = selectedRegion.toLowerCase().replace(/\s+/g, '');
        showCard = region.includes(selected) || selected.includes(region);
      }

      if (showCard && selectedState && selectedState !== "") {
        const state = card.querySelector(".post-status")?.textContent.trim() || "";
        showCard = state === selectedState;
      }

      card.style.display = showCard ? "block" : "none";
    });
  }
});