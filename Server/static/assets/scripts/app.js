document.addEventListener("DOMContentLoaded", function () {

  const headerDesktopNavbarItems = document.querySelectorAll('#header-desktop-navbar ul');
  const headerDesktopIndicator = document.querySelector("#header-desktop-navbar-indicator");

  const updateIndicatorStyle = (offsetWidth, offsetLeft, dataset) => {
    const isDarkMode = document.documentElement.classList.contains("dark");
    const backgroundColor = isDarkMode ? dataset.colorDark || '#34d399' : dataset.colorLight || '#10b981';
    headerDesktopIndicator.style.cssText = `width: ${offsetWidth}px; left: ${offsetLeft}px; background-color: ${backgroundColor};`;
  };

  const indicatorHandlerStart = (e) => updateIndicatorStyle(e.offsetWidth, e.offsetLeft, e.dataset);
  const indicatorHandlerEnd = () => headerDesktopIndicator.style.width = 0;

  headerDesktopNavbarItems.forEach((item) => {
    item.addEventListener("mouseover", () => indicatorHandlerStart(item));
    item.addEventListener("mouseleave", indicatorHandlerEnd);
  });

  const indicatorHandlerInitial = (e) => {
    const { offsetLeft, dataset } = e;
    updateIndicatorStyle(0, offsetLeft, dataset);
  };

  indicatorHandlerInitial(headerDesktopNavbarItems[0]);
  // Scroll Top Function Start
  const scrollTopFooter = document.getElementById("scroll-top-button-footer");
  if (scrollTopFooter)
    scrollTopFooter.addEventListener("click", () =>
      window.scrollTo({ top: 0, behavior: "smooth" }),
    );

  // Scroll Top Function End

  // Theme Section Start
  const theme = {
    current: localStorage.getItem("theme"),
    toggleDesktop: document.getElementById("toggleThemeDesktop"),
    toggleMobile: document.getElementById("toggleThemeMobile"),
    iconDesktop: document.getElementById("themeIconDesktop"),
    iconMobile: document.getElementById("themeIconMobile"),
    text: document.getElementById("themeText"),
  };

  if (theme.iconDesktop && theme.iconMobile) {
    const setThemeInfo = (mode) => {
      const isDark = mode === "dark";
      if (theme.iconDesktop)
        theme.iconDesktop.innerHTML = `<use xlink:href="#${isDark ? "sun" : "moon"}" />`;
      if (theme.iconMobile && theme.text) {
        theme.iconMobile.innerHTML = `<use xlink:href="#${isDark ? "sun" : "moon"}" />`;
        theme.text.innerHTML = `حالت ${isDark ? "شب" : "روز"}`;
      }

    };

    setThemeInfo(theme.current);

    const toggleTheme = () => {
      const isDarkMode = document.documentElement.classList.toggle("dark");
      setThemeInfo(isDarkMode ? "dark" : "light");
      localStorage.setItem("theme", isDarkMode ? "dark" : "light");
    };
    const isDark = () => {
      return document.documentElement.classList.contains("dark");
    };

    const isAppearanceTransition =
      typeof document !== "undefined" &&
      document.startViewTransition &&
      !window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    function toggleDark(event) {
      if (!isAppearanceTransition || !event) {
        toggleTheme();
        return;
      }

      const x = event.clientX;
      const y = event.clientY;
      const endRadius = Math.hypot(
        Math.max(x, innerWidth - x),
        Math.max(y, innerHeight - y)
      );

      const transition = document.startViewTransition(async () => {
        toggleTheme();
      });

      transition.ready.then(() => {
        const clipPath = [
          `circle(0px at ${x}px ${y}px)`,
          `circle(${endRadius}px at ${x}px ${y}px)`,
        ];
        document.documentElement.animate(
          {
            clipPath: isDark() ? [...clipPath].reverse() : clipPath,
          },
          {
            duration: 500,
            easing: "ease-in",
            pseudoElement: isDark()
              ? "::view-transition-old(root)"
              : "::view-transition-new(root)",
          }
        );
      });
    }

    theme.toggleDesktop.addEventListener("click", toggleDark);
    theme.toggleMobile.addEventListener("click", toggleDark);
  }
  // Theme Section End


  // Header Scripts Section Start

  // Toggle Desktop Mega menu ( Categories )
  const desktopMegamenuWrapper = document.getElementById("desktopMegamenuWrapper");
  const desktopMegamenu = document.getElementById("desktopMegamenu");
  const headerOverlay = document.getElementById("header-overlay");
  let showDesktopMegamenu = false;

  if (desktopMegamenuWrapper && desktopMegamenu && headerOverlay) {

    const toggleMegamenu = (event) => {
      showDesktopMegamenu = event.type === "mouseenter";
      desktopMegamenu.classList.toggle("hidden", !showDesktopMegamenu);
      headerOverlay.classList.toggle("hidden", !showDesktopMegamenu);
    };

    desktopMegamenuWrapper.addEventListener("mouseenter", toggleMegamenu);
    desktopMegamenuWrapper.addEventListener("mouseleave", toggleMegamenu);
  }


  // Hide mobile navbar on Scroll Start
  let isSearchResultShow = false
  const mobileHeaderBottom = document.getElementById("mobile-header-bottom");
  const desktopHeaderBottom = document.getElementById("desktop-header-bottom");
  let isScrollingDown = false;
  let prevScrollPos = window.pageYOffset || document.documentElement.scrollTop;


  if (mobileHeaderBottom && desktopHeaderBottom) {
    const handleScroll = () => {
      const currentScrollPos =
        window.pageYOffset || document.documentElement.scrollTop;

      if (currentScrollPos > 100 && currentScrollPos > prevScrollPos) {
        if (!isScrollingDown && !showDesktopMegamenu && !isSearchResultShow) {
          mobileHeaderBottom.classList.add("-translate-y-full");
          desktopHeaderBottom.classList.add("-translate-y-full");
          isScrollingDown = true;
        }
      } else {
        mobileHeaderBottom.classList.remove("-translate-y-full");
        desktopHeaderBottom.classList.remove("-translate-y-full");
        isScrollingDown = false;
      }

      prevScrollPos = currentScrollPos;
    };

    window.addEventListener("scroll", handleScroll);
  }
  // Hide mobile navbar on Scroll End


  // Desktop Header Megamenu section
  const categoriesParentsMegamenu = document.querySelectorAll(
    "#mega-menu-parents li a",
  );
  const categoriesChildsMegamenu = document.querySelectorAll(
    "#mega-menu-childs > div[data-category-child]",
  );

  if (categoriesParentsMegamenu.length > 0) {
    // Apply the classes to the first item at page load
    categoriesParentsMegamenu[0].classList.add("mega-menu-active");
    categoriesChildsMegamenu[0].classList.remove("hidden");

    categoriesParentsMegamenu.forEach((item) => {
      item.addEventListener("mouseenter", () => {
        // Remove the 'active' class from all parent categories and hide all child divs
        categoriesParentsMegamenu.forEach((otherItem) =>
          otherItem.classList.remove("mega-menu-active")
        );
        categoriesChildsMegamenu.forEach((childDiv) =>
          childDiv.classList.add("hidden")
        );

        // Add the 'active' class to the current parent category and show the corresponding child div
        item.classList.add("mega-menu-active");
        document
          .querySelector(`div[data-category-child="${item.getAttribute("data-category-parent")}"]`)
          .classList.remove("hidden");
      });
    });
  }
  // Header Scripts Section End

  new Swiper(".banner-slider", {
    pagination: {
      el: ".swiper-pagination",
      dynamicBullets: true,
    },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
    loop: true,
    autoplay: {
      delay: 3000,
    },
  });

  new Swiper(".product-slider", {
    slidesPerView: 1.5,
    spaceBetween: 14,
    freeMode: true,
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },

    breakpoints: {
      360: {
        slidesPerView: 2,
        spaceBetween: 10,
      },
      460: {
        slidesPerView: 2.5,
        spaceBetween: 10,
      },
      640: {
        slidesPerView: 3,
        spaceBetween: 10,
      },
      768: {
        slidesPerView: 3.5,
        spaceBetween: 10,
      },
      1024: {
        slidesPerView: 4.5,
        spaceBetween: 10,
      },
      1380: {
        slidesPerView: 6,
        spaceBetween: 10,
      },
    },
  });
  new Swiper(".product-slider-wrapped", {
    slidesPerView: 1.7,
    spaceBetween: 2,
    freeMode: true,
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },

    breakpoints: {
      360: {
        slidesPerView: 2,
        spaceBetween: 2,
      },
      460: {
        slidesPerView: 2.5,
        spaceBetween: 2,
      },
      640: {
        slidesPerView: 3,
        spaceBetween: 2,
      },
      768: {
        slidesPerView: 3.5,
        spaceBetween: 2,
      },
      1024: {
        slidesPerView: 4.5,
        spaceBetween: 2,
      },
      1380: {
        slidesPerView: 6,
        spaceBetween: 2,
      },
    },
  });
  new Swiper(".product-image-mobile-swiper", {
    pagination: {
      el: ".swiper-pagination",
    },
  });
  const product_gallery_image_desktop2 = new Swiper(
    ".product-image-desktop-2-swiper",
    {
      slidesPerView: 8,
      spaceBetween: 20,
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
    },
  );
  new Swiper(".product-image-desktop-swiper", {
    thumbs: {
      swiper: product_gallery_image_desktop2,
      slideThumbActiveClass: "swiper-thumb-active",
    },
    pagination: {
      el: ".swiper-pagination",
    },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
  });

  new Swiper(".product-comments-swiper", {
    slidesPerView: 1.1,
    spaceBetween: 10,
    freeMode: true,

    breakpoints: {
      360: {
        slidesPerView: 1.2,
        spaceBetween: 10,
      },
      460: {
        slidesPerView: 1.6,
        spaceBetween: 10,
      },
      640: {
        slidesPerView: 2.2,
        spaceBetween: 10,
      },
    },
  });
  new Swiper(".orders-product-swiper", {
    slidesPerView: 1.1,
    spaceBetween: 10,
    freeMode: true,

    breakpoints: {
      360: {
        slidesPerView: 1.2,
        spaceBetween: 10,
      },
      460: {
        slidesPerView: 1.6,
        spaceBetween: 10,
      },
      640: {
        slidesPerView: 2.2,
        spaceBetween: 10,
      },
      1380: {
        slidesPerView: 3.1,
        spaceBetween: 10,
      },
    },
  });
  new Swiper(".notifications-product-swiper", {
    slidesPerView: 1.1,
    spaceBetween: 10,
    freeMode: true,

    breakpoints: {
      360: {
        slidesPerView: 1.2,
        spaceBetween: 10,
      },
      460: {
        slidesPerView: 1.6,
        spaceBetween: 10,
      },
      640: {
        slidesPerView: 2.2,
        spaceBetween: 10,
      },
      1380: {
        slidesPerView: 3.1,
        spaceBetween: 10,
      },
    },
  });

  new Swiper(".blog-slider", {
    slidesPerView: 1.7,
    spaceBetween: 14,
    freeMode: true,
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },

    breakpoints: {
      360: {
        slidesPerView: 2,
        spaceBetween: 10,
      },
      460: {
        slidesPerView: 2.5,
        spaceBetween: 15,
      },
      640: {
        slidesPerView: 3,
        spaceBetween: 10,
      },
      768: {
        slidesPerView: 3.2,
        spaceBetween: 15,
      },
      1024: {
        slidesPerView: 4,
        spaceBetween: 20,
      },
      1380: {
        slidesPerView: 4,
        spaceBetween: 20,
      },
    },
  });
  new Swiper(".search-result-desktop", {
    slidesPerView: 1.3,
    spaceBetween: 10,
    freeMode: true,
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },

    breakpoints: {
      360: {
        slidesPerView: 1.5,
        spaceBetween: 10,
      },
      460: {
        slidesPerView: 2.1,
        spaceBetween: 10,
      },
      640: {
        slidesPerView: 2.5,
        spaceBetween: 10,
      },
      768: {
        slidesPerView: 2.1,
        spaceBetween: 10,
      },
      1024: {
        slidesPerView: 2.2,
        spaceBetween: 10,
      },
      1380: {
        slidesPerView: 2.5,
        spaceBetween: 10,
      },
    },
  });
  // Border Animation Section Start
  const setMousePosition = (e) => {
    document.querySelectorAll(".border-gradient").forEach((item) => {
      const { left, top } = item.getBoundingClientRect();
      const { clientX, clientY } = e;
      item.style.setProperty("--x", `${clientX - left}px`);
      item.style.setProperty("--y", `${clientY - top}px`);
    });
  };

  document.addEventListener("mousemove", setMousePosition);

  // Border Animation Section End

  // noUiSlider Section Start

  const shopPriceSlider = document.querySelectorAll("#shop-price-slider");
  const shopPriceSliderMin = document.querySelectorAll(
    "#shop-price-slider-min",
  ),
    shopPriceSliderMax = document.querySelectorAll("#shop-price-slider-max");

  shopPriceSlider.forEach((item) => {
    noUiSlider.create(item, {
      cssPrefix: "range-slider-",
      start: [0, 100_000_000],
      direction: "rtl",
      margin: 1,
      connect:true,
      range: {
        min: 0,
        max: 100_000_000,
      },
      format: {
        to: function (value) {
          return value.toLocaleString("en-US", {
            style: "decimal",
            maximumFractionDigits: 0,
          });
        },
        from: function (value) {
          return parseFloat(value.replace(/,/g, ""));
        },
      },
    });

    item.noUiSlider.on("update", function (values, handle) {
      if (handle) {
        shopPriceSliderMax.forEach((price_item) => {
          price_item.innerHTML = values[handle];
        });
      } else {
        shopPriceSliderMin.forEach((price_item) => {
          price_item.innerHTML = values[handle];
        });
      }
    });
  });
  // noUiSlider Section End

  // Header Search Overlay Start
  function initializeSearchComponent(baseId, wrapperId, searchId, resultId) {
    const base = document.getElementById(baseId);
    const wrapper = document.getElementById(wrapperId);
    const search = document.getElementById(searchId);
    const result = document.getElementById(resultId);

    if (!base || !wrapper || !search || !result) {
      return;
    }

    function hideSearchResults() {
      wrapper.classList.remove(
        "border",
        "bg-primary-light",
        "dark:bg-secondary-dark",
        "rounded-b-none"
      );
      wrapper.classList.add("bg-secondary-light", "dark:bg-primary-dark");
      search.classList.remove("bg-primary-light", "dark:bg-secondary-dark");
      search.classList.add("bg-secondary-light", "dark:bg-primary-dark");
      wrapper.classList.remove("rounded-b-none");
      headerOverlay.classList.add("hidden");
      result.classList.add("hidden");
      isSearchResultShow = false;
    }

    search.addEventListener("focus", () => {
      wrapper.classList.add(
        "border",
        "bg-primary-light",
        "dark:bg-secondary-dark",
        "rounded-b-none"
      );
      wrapper.classList.remove("bg-secondary-light", "dark:bg-primary-dark");
      search.classList.add("bg-primary-light", "dark:bg-secondary-dark");
      search.classList.remove("bg-secondary-light", "dark:bg-primary-dark");
      headerOverlay.classList.remove("hidden");
      result.classList.remove("hidden");
      isSearchResultShow = true;
    });

    return { base, hideSearchResults };
  }

  const desktopSearchComponent = initializeSearchComponent(
    "desktopHeaderSearchBase",
    "desktopHeaderSearchWrapper",
    "desktopHeaderSearch",
    "desktopHeaderSearchResult"
  );

  const mobileSearchComponent = initializeSearchComponent(
    "mobileHeaderSearchBase",
    "mobileHeaderSearchWrapper",
    "mobileHeaderSearch",
    "mobileHeaderSearchResult"
  );

  if (desktopSearchComponent && mobileSearchComponent) {
    const { base: desktopBase, hideSearchResults: hideDesktopSearchResults } = desktopSearchComponent;
    const { base: mobileBase, hideSearchResults: hideMobileSearchResults } = mobileSearchComponent;

    // Add click event listener to the document
    document.addEventListener("mousedown", (event) => {
      if (
        desktopBase && mobileBase &&
        !desktopBase.contains(event.target) &&
        !mobileBase.contains(event.target)
      ) {
        hideDesktopSearchResults();
        hideMobileSearchResults();
      }
    });
  }
  // Header Search Overlay End



// Quiantity Input Start
function quantityDecrement(e) {

  const btn = e.target.parentNode.parentElement.querySelector(
    'button[data-action="increment"]'
  );
  if (btn) {
    const target = btn.nextElementSibling;
    if (target) {
      let value = Number(target.value);
      const min = target.hasAttribute("min") ? Number(target.min) : -Infinity;
      const max = target.hasAttribute("max") ? Number(target.max) : Infinity;
      if (value == 1) return
      // Check if value is greater than the minimum allowed value
      if (isNaN(min) || value > min) {
        value--;
      }

      // Update only if value is less than or equal to the maximum allowed value
      if (isNaN(max) || value <= max) {
        target.value = value;
      }
    }
  }

}

function quantityIncrement(e) {

  const btn = e.target.parentNode.parentElement.querySelector(
    'button[data-action="increment"]'
  );
  if (btn) {
    const target = btn.nextElementSibling;
    if (target) {

      let value = Number(target.value);
      const min = target.hasAttribute("min") ? Number(target.min) : -Infinity;
      const max = target.hasAttribute("max") ? Number(target.max) : Infinity;

      // Check if value is less than the maximum allowed value
      if (isNaN(max) || value < max) {
        value++;
      }

      // Update only if value is greater than or equal to the minimum allowed value
      if (isNaN(min) || value >= min) {
        target.value = value;
      }

    }
  }
}

  const quantityDecrementButtons = document.querySelectorAll(
    `button[data-action="decrement"]`
  );

  const quantityIncrementButtons = document.querySelectorAll(
    `button[data-action="increment"]`
  );

  quantityDecrementButtons.forEach(btn => {
    btn.addEventListener("click", quantityDecrement);
  });

  quantityIncrementButtons.forEach(btn => {
    btn.addEventListener("click", quantityIncrement);
  });
  // Quiantity Input End
});

