function reportBtn(){
  if(confirm("신고하시겠습니까?")){
    alert("신고되었습니다.");
  }else{
    alert("취소");
  }
}

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
document.querySelectorAll(".board-item").forEach(item => {
item.addEventListener("click", (e) => {
    if (e.target.closest('.report-btn')) return;

    const artistText = item.querySelector(".artist")?.textContent.trim();
    const onoffText = item.querySelector(".onoff")?.textContent.trim();
    const TwayText = item.querySelector(".Tway")?.textContent.trim();
    const title = item.querySelector(".board-title")?.textContent.trim();
    const star = item.querySelector(".star")?.textContent.trim();
    const desc = item.querySelector(".board-preview, .board-content")?.textContent.trim();
    const writer = item.querySelector(".writer_id")?.textContent.trim();
    const partner = item.querySelector(".partner_id")?.textContent.trim();
    const date = item.querySelector(".post-date")?.textContent.trim(); // 날짜 추가
    const images = item.getAttribute("data-images")?.split(",") || [];
    const tags = Array.from(item.querySelectorAll(".post-tag")).map(tag => tag.textContent.trim());

    openPostModal(artistText, onoffText, TwayText, title, `${writer} ⇄ ${partner}`, star, desc, images, tags, date);
});
});

function openPostModal(artistText, onoffText, TwayText, title, writerPartner, star, desc, imageUrls = [], tags = [], date = "") {
const [writer, partner] = writerPartner.split(" ⇄ ");

const artistEl = document.getElementById("modalPostArtist");
const onoffEl = document.getElementById("modalPostOnoff");
const TwayEl = document.getElementById("modalPostTway");

artistEl.textContent = artistText;
artistEl.className = "artist";

onoffEl.textContent = onoffText;
onoffEl.className = "onoff";

TwayEl.textContent = TwayText;
TwayEl.className = "Tway";

document.getElementById("modalPostTitle").textContent = title;
document.getElementById("modalPostWriter").textContent = `${writer}`;
document.getElementById("modalPostPartner").textContent = `🔄 ${partner}`;
document.getElementById("modalPostStar").textContent = `${star}`;
document.getElementById("modalPostDescription").textContent = desc;
document.getElementById("modalPostDate").textContent = date; // 날짜 설정

const tagsContainer = document.getElementById("modalPostTags");
tagsContainer.innerHTML = "";

    if (tags.length > 0) {
      tags.forEach(tag => {
        const span = document.createElement("span");
        span.className = "post-tag";
        span.textContent = tag;
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
});

document.addEventListener("DOMContentLoaded", function () {
  const generalInput = document.getElementById("generalSearch");
  const tagInput = document.getElementById("tagSearch");
  const ratingFilter = document.getElementById("ratingFilter");
  const sortFilter = document.getElementById("sortFilter");
  const toggleBtns = document.querySelectorAll(".toggle-btn");
  const boardItems = Array.from(document.querySelectorAll(".board-item"));

  // 🔁 토글 버튼 클릭 시 검색 입력창 전환
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
      applyFilters(); // 즉시 반영
    });
  });

  // 🎯 검색/필터/정렬 이벤트 바인딩
  generalInput.addEventListener("input", applyFilters);
  tagInput.addEventListener("input", applyFilters);
  ratingFilter.addEventListener("change", applyFilters);
  sortFilter.addEventListener("change", applyFilters);

  function applyFilters() {
    const searchMode = document.querySelector(".toggle-btn.active").dataset.type;
    const keyword = (searchMode === "general" ? generalInput.value : tagInput.value).toLowerCase();
    const selectedRating = ratingFilter.value;
    const sortBy = sortFilter.value;

    let filtered = boardItems.filter(item => {
      const title = item.querySelector(".board-title")?.textContent.toLowerCase() || "";
      const writer = item.querySelector(".writer_id")?.textContent.toLowerCase() || "";
      const partner = item.querySelector(".partner_id")?.textContent.toLowerCase() || "";
      const tags = Array.from(item.querySelectorAll(".post-tag")).map(tag => tag.textContent.toLowerCase());
      const star = item.querySelector(".star")?.textContent.replace("⭐", "").trim();

      document.getElementById('sortFilter').addEventListener('change', function() {
    const sortType = this.value;
    sortPosts(sortType);
});

    // 정렬 필터 이벤트 리스너 추가
document.getElementById('sortFilter').addEventListener('change', function() {
    const sortType = this.value;
    sortPosts(sortType);
});

// 게시글 정렬 함수
function sortPosts(sortType) {
    const boardList = document.querySelector('.board-list');
    const boardItems = Array.from(boardList.querySelectorAll('.board-item'));
    
    let sortedItems;
    
    switch(sortType) {
        case 'latest':
            // 최신순 정렬 (날짜 기준 내림차순)
            sortedItems = boardItems.sort((a, b) => {
                const dateA = new Date(a.querySelector('.post-date').textContent);
                const dateB = new Date(b.querySelector('.post-date').textContent);
                return dateB - dateA; // 내림차순
            });
            break;
            
        case 'rating':
            // 평점순 정렬 (별점 기준 내림차순)
            sortedItems = boardItems.sort((a, b) => {
                const ratingA = parseInt(a.querySelector('.star').textContent.match(/\d+/)[0]);
                const ratingB = parseInt(b.querySelector('.star').textContent.match(/\d+/)[0]);
                return ratingB - ratingA; // 내림차순
            });
            break;
            
        case 'views':
            // 조회순 정렬 (조회수 기준 내림차순)
            sortedItems = boardItems.sort((a, b) => {
                const viewsA = parseInt(a.querySelector('.board-meta span:last-child').textContent.match(/\d+/)[0]);
                const viewsB = parseInt(b.querySelector('.board-meta span:last-child').textContent.match(/\d+/)[0]);
                return viewsB - viewsA; // 내림차순
            });
            break;
            
        case '':
        default:
            // 기본 정렬 (원래 순서 유지)
            sortedItems = boardItems;
            return; // 빈 값일 때는 정렬하지 않음
    }
    
    // 기존 게시글들 제거
    boardItems.forEach(item => item.remove());
    
    // 정렬된 게시글들 다시 추가
    sortedItems.forEach(item => boardList.appendChild(item));
}

      // 검색 필터
      let matchSearch = true;
      if (keyword) {
        if (searchMode === "general") {
          matchSearch = title.includes(keyword) || writer.includes(keyword) || partner.includes(keyword);
        } else {
          matchSearch = tags.some(tag => tag.includes(keyword));
        }
      }

      // 평점 필터
      let matchRating = true;
      if (selectedRating) {
        matchRating = star === selectedRating;
      }

      return matchSearch && matchRating;
    });

    // 정렬
    filtered.sort((a, b) => {
      if (sortBy === "latest") {
        return boardItems.indexOf(a) - boardItems.indexOf(b);
      } else if (sortBy === "rating") {
        const aRating = parseFloat(a.querySelector(".star")?.textContent.replace("⭐", "").trim() || 0);
        const bRating = parseFloat(b.querySelector(".star")?.textContent.replace("⭐", "").trim() || 0);
        return bRating - aRating;
      } else if (sortBy === "views") {
        const aViews = parseInt(a.querySelector(".board-meta span:last-child")?.textContent.replace("👁️", "").trim() || 0);
        const bViews = parseInt(b.querySelector(".board-meta span:last-child")?.textContent.replace("👁️", "").trim() || 0);
        return bViews - aViews;
      }
    });

    // 다시 그리기
    const container = document.querySelector(".board-list");
    container.innerHTML = "";
    filtered.forEach(item => container.appendChild(item));
  }
});