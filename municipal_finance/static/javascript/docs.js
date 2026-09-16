$(() => {
  $.ajax({
    url: '/api/cubes',
  }).done((response) => {
    $('#get-cubes').text(JSON.stringify(response, null, 2));
  });
});

(function (exports) {
  var MainView = Backbone.View.extend({
    el: document,

    events: {
      'click button.accept': 'acceptTOU',
      'click button.decline': 'declineTOU',
    },

    initialize() {
      // show terms of use dialog?
      if (!Cookies.get('tou-ok')) {
        $('#terms-modal').modal();
      } else {
        this.acceptTOU();
      }
    },

    showTOU() {
      $('#terms-modal').modal();
    },

    acceptTOU() {
      Cookies.set('tou-ok', true);
      $('#terms-modal').modal('hide');
      $('#terms-ok').removeClass('hidden');
    },

    declineTOU() {
      Cookies.remove('tou-ok');
      window.location = '/';
    },
  });

  exports.view = new MainView();
}(window));

(function () {
  var MAX_DIRECT_DOWNLOADS = 10;
  var DOWNLOAD_INTERVAL_MS = 1500;
  var SCRIPT_NAME = 'municipal-money-bulk-download.sh';

  var $table = $('#bulk-downloads');
  if (!$table.length) return;

  var $summary = $('#bulk-selection-summary');
  var $downloadSelected = $('#bulk-download-selected');
  var $downloadScript = $('#bulk-download-script');

  function selected() {
    return $table.find('.bulk-file-check:checked');
  }

  function refreshParent($parent, $children) {
    var total = $children.length;
    var checked = $children.filter(':checked').length;
    $parent.prop('checked', total > 0 && checked === total);
    $parent.prop('indeterminate', checked > 0 && checked < total);
  }

  function refresh() {
    $table.find('tbody.bulk-cube').each(function () {
      var $cube = $(this);
      refreshParent($cube.find('.bulk-cube-check'), $cube.find('.bulk-file-check'));
    });
    var count = selected().length;

    if (count === 0) {
      $summary.text('No files selected');
    } else {
      $summary.text(`${count} ${count === 1 ? 'file' : 'files'} selected`);
    }

    $downloadSelected.prop('disabled', count === 0);
    $downloadScript.prop('disabled', count === 0);
  }

  function downloadInBackground(url) {
    var iframe = document.createElement('iframe');
    iframe.style.display = 'none';
    iframe.src = url;
    document.body.appendChild(iframe);
    window.setTimeout(() => {
      document.body.removeChild(iframe);
    }, 120000);
  }

  function buildScript($selected) {
    var lines = [
      '#!/bin/sh',
      '# Municipal Money bulk download',
      `# Generated ${new Date().toISOString()}`,
      '#',
      `# Downloads the files selected on ${window.location.origin}/docs#bulkdownloads`,
      '# Re-running the script resumes any partial downloads rather than',
      '# starting them again.',
      '',
      'set -e',
      '',
      'download() {',
      '  if command -v curl > /dev/null 2>&1; then',
      '    curl -fL -C - -o "$2" "$1"',
      '  elif command -v wget > /dev/null 2>&1; then',
      '    wget -c -O "$2" "$1"',
      '  else',
      '    echo "Needs either curl or wget on your PATH." >&2',
      '    exit 1',
      '  fi',
      '}',
      '',
    ];

    $selected.each(function () {
      var $file = $(this);
      lines.push(`download "${$file.data('url')}" "${$file.data('name')}"`);
    });

    lines.push('');
    lines.push('cat > md5sums.txt <<\'EOF\'');
    $selected.each(function () {
      var $file = $(this);
      lines.push(`${$file.data('md5')}  ${$file.data('name')}`);
    });
    lines.push('EOF');
    lines.push('');
    lines.push('echo "Verifying checksums..."');
    lines.push('if command -v md5sum > /dev/null 2>&1; then');
    lines.push('  md5sum -c md5sums.txt');
    lines.push('elif command -v md5 > /dev/null 2>&1; then');
    lines.push('  echo "Compare against md5sums.txt:"');
    lines.push('  md5 -r *.csv *.xlsx 2> /dev/null || true');
    lines.push('else');
    lines.push('  echo "No md5 tool found; checksums left in md5sums.txt."');
    lines.push('fi');
    lines.push('');

    return lines.join('\n');
  }

  $table.on('change', '.bulk-file-check', refresh);

  $table.on('change', '.bulk-cube-check', function () {
    var checked = $(this).prop('checked');
    $(this).closest('tbody.bulk-cube').find('.bulk-file-check').prop('checked', checked);
    refresh();
  });

  $downloadSelected.on('click', () => {
    var $selected = selected();
    if (!$selected.length) return;

    if ($selected.length > MAX_DIRECT_DOWNLOADS) {
      window.alert(
        `You have selected ${$selected.length} files. Browsers handle more than `
        + `${MAX_DIRECT_DOWNLOADS} downloads at once poorly, and a failed `
        + 'download cannot be resumed.\n\n'
        + 'Use "Download script" instead -- it fetches the same files, resumes '
        + 'where it left off, and verifies them.',
      );
      return;
    }

    $selected.each(function (index) {
      var url = $(this).data('url');
      window.setTimeout(() => {
        downloadInBackground(url);
      }, index * DOWNLOAD_INTERVAL_MS);
    });
  });

  $downloadScript.on('click', () => {
    var $selected = selected();
    if (!$selected.length) return;

    var blob = new Blob([buildScript($selected)], { type: 'text/x-shellscript' });
    var url = URL.createObjectURL(blob);
    var link = document.createElement('a');
    link.href = url;
    link.download = SCRIPT_NAME;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  });

  refresh();
}());
