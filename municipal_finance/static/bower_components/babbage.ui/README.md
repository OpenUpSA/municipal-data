# babbage.ui

[![Gitter](https://img.shields.io/gitter/room/openspending/chat.svg)](https://gitter.im/openspending/chat)

The library provides a DSL, query frontend and visualisation functions running against the [Babbage Analytical Engine](https://github.com/spendb/babbage) API. The intent is to make a re-usable set of angular-based front-end
components for business intelligence.

### Usage

```html
<babbage slicer="http://host.org/slicer" cube="sales">
    <div class="row">
        <div class="col-md-4">
            <babbage-filter-panel></babbage-filter-panel>
        </div>
        <div class="col-md-8">
            <babbage-table></babbage-table>
        </div>
    </div>
</babbage>
```

Or, with inline config:

```html
<babbage slicer="http://host.org/slicer" cube="sales">
    <babbage-treemap drilldown="region" measure="sales_usd" cut="time.year:2015">
    </babbage-treemap>
</babbage>
```

### Example

Clone the repository and open ``index.html`` to see ``babbage`` in action, no pre-config required.

### Dev installation

* Dev tool installation with [npm](https://www.npmjs.com/): ``npm install`` (see ``package.json``)
* Web packaging with [Bower](http://bower.io/): ``bower install`` (see ``bower.json``)
* Build automation with [Grunt](http://gruntjs.com/): ``grunt`` without arguments runs the ``default`` task (see ``Gruntfile.js``)

### A few links

* [Sample API result](https://spendb-dev.herokuapp.com/api/slicer/cube/wb-contract-awards/aggregate?drilldown=supplier_country)
* [vega tutorial](https://github.com/trifacta/vega/wiki/Tutorial)
* [nvd3](https://github.com/novus/nvd3) and [angular-nvd3](https://github.com/krispo/angular-nvd3)
* [OffenerHaushalt Treemaps](https://github.com/okfde/offenerhaushalt.de/blob/master/offenerhaushalt/static/js/treemap.js)
