(function() {
  "use strict";

  const select = (el, all = false) => {
    el = el.trim();
    if (all) {
      return [...document.querySelectorAll(el)];
    } else {
      return document.querySelector(el);
    }
  };

  const on = (type, el, listener, all = false) => {
    if (all) {
      select(el, all).forEach(e => e.addEventListener(type, listener));
    } else {
      select(el, all).addEventListener(type, listener);
    }
  };

  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener);
  };

  if (select('.toggle-sidebar-btn')) {
    on('click', '.toggle-sidebar-btn', function(e) {
      select('body').classList.toggle('toggle-sidebar');
    });
  }

  if (select('.search-bar-toggle')) {
    on('click', '.search-bar-toggle', function(e) {
      select('.search-bar').classList.toggle('search-bar-show');
    });
  }

  let navbarlinks = select('#navbar .scrollto', true);
  const navbarlinksActive = () => {
    let position = window.scrollY + 200;
    navbarlinks.forEach(navbarlink => {
      if (!navbarlink.hash) return;
      let section = select(navbarlink.hash);
      if (!section) return;
      if (
        position >= section.offsetTop &&
        position <= section.offsetTop + section.offsetHeight
      ) {
        navbarlink.classList.add('active');
      } else {
        navbarlink.classList.remove('active');
      }
    });
  };
  window.addEventListener('load', navbarlinksActive);
  onscroll(document, navbarlinksActive);

  let selectHeader = select('#header');
  if (selectHeader) {
    const headerScrolled = () => {
      if (window.scrollY > 100) {
        selectHeader.classList.add('header-scrolled');
      } else {
        selectHeader.classList.remove('header-scrolled');
      }
    };
    window.addEventListener('load', headerScrolled);
    onscroll(document, headerScrolled);
  }

  let backtotop = select('.back-to-top');
  if (backtotop) {
    const toggleBacktotop = () => {
      if (window.scrollY > 100) {
        backtotop.classList.add('active');
      } else {
        backtotop.classList.remove('active');
      }
    };
    window.addEventListener('load', toggleBacktotop);
    onscroll(document, toggleBacktotop);
  }

  var tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // Quill editors
  if (select('.quill-editor-default')) {
    new Quill('.quill-editor-default', {
      theme: 'snow'
    });
  }
  if (select('.quill-editor-bubble')) {
    new Quill('.quill-editor-bubble', {
      theme: 'bubble'
    });
  }
  if (select('.quill-editor-full')) {
    new Quill('.quill-editor-full', {
      modules: {
        toolbar: [
          [{ font: [] }, { size: [] }],
          ['bold', 'italic', 'underline', 'strike'],
          [{ color: [] }, { background: [] }],
          [{ script: 'super' }, { script: 'sub' }],
          [{ list: 'ordered' }, { list: 'bullet' }, { indent: '-1' }, { indent: '+1' }],
          ['direction', { align: [] }],
          ['link', 'image', 'video'],
          ['clean']
        ]
      },
      theme: 'snow'
    });
  }

  /*
   * TinyMCE отключён
   */

  var needsValidation = document.querySelectorAll('.needs-validation');
  Array.prototype.slice.call(needsValidation).forEach(function(form) {
    form.addEventListener(
      'submit',
      function(event) {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      },
      false
    );
  });

  const datatables = select('.datatable', true);
  datatables.forEach(datatable => {
    new simpleDatatables.DataTable(datatable, {
      perPageSelect: [5, 10, 15, ['All', -1]],
      columns: [
        { select: 2, sortSequence: ['desc', 'asc'] },
        { select: 3, sortSequence: ['desc'] },
        { select: 4, cellClass: 'green', headerClass: 'red' }
      ]
    });
  });

  const mainContainer = select('#main');
  if (mainContainer) {
    setTimeout(() => {
      new ResizeObserver(function() {
        select('.echart', true).forEach(getEchart => {
          echarts.getInstanceByDom(getEchart).resize();
        });
      }).observe(mainContainer);
    }, 200);
  }

  // ** Отладочные логи кнопок **
  let taskButtons = select('.btn', true);
  taskButtons.forEach(button => {
    console.log("Кнопка найдена: ", button);
    if (button.classList.contains('btn-success')) {
      console.log("Кнопка 'Запустить' активна или отключена:", button.disabled);
    } else if (button.classList.contains('btn-warning')) {
      console.log("Кнопка 'Остановить' активна или отключена:", button.disabled);
    }
  });
  const startButtons = document.querySelectorAll('.btn-success');
  startButtons.forEach(button => {
    const progressBar = button.closest('tr').querySelector('.progress-bar');
    const progress = progressBar ? progressBar.style.width : '0%';
    console.log(`Прогресс задачи: ${progress}`);
    console.log(`Кнопка 'Запустить' для задачи со статусом ${progress}. Состояние кнопки: ${button.disabled ? 'Заблокирована' : 'Активна'}`);
  });

  // ---------------------------
  //  Сохранение/восстановление панели

  // 1) все формы запуска/остановки помечены классом .js-preserve-panel
  document.querySelectorAll('form.js-preserve-panel').forEach(form => {
    form.addEventListener('submit', () => {
      const item = form.closest('.accordion-item');
      if (item && item.dataset.orderId) {
        localStorage.setItem('lastOpenOrder', item.dataset.orderId);
      }
    });
  });

  // 2) после загрузки восстанавливаем последнюю открытую панель
  document.addEventListener('DOMContentLoaded', () => {
    const last = localStorage.getItem('lastOpenOrder');
    if (last) {
      // закрываем все
      document.querySelectorAll('#ordersAccordion .accordion-collapse.show')
        .forEach(el => el.classList.remove('show'));
      document.querySelectorAll('#ordersAccordion .accordion-button:not(.collapsed)')
        .forEach(btn => btn.classList.add('collapsed'));
      // открываем нужную
      const panel = document.getElementById(`collapse-${last}`);
      const headerBtn = document.querySelector(`[data-bs-target="#collapse-${last}"]`);
      if (panel && headerBtn) {
        panel.classList.add('show');
        headerBtn.classList.remove('collapsed');
      }
      localStorage.removeItem('lastOpenOrder');
    }
  });

})();
