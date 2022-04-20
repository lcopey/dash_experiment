window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        copy_function: function(keydown, selected_cells, data) {
            if (keydown) {
                if (keydown['ctrlKey'] & (keydown['key'] === 'c')) {
                    console.log(keydown);
                    console.log(selected_cells);
                    console.log(data);

                    for (const item of selected_cells) {
                        console.log(data[item['row']][item['column_id']])
                    }
                    return '';
                }
            }
            return ''
        }
    }
});
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        test: function() {
            console.log('test')
        },
        synchronize_columns_mapping: function(columns) {
            return columns.reduce((obj, cur) => ({...obj, [cur.sid]: cur}), {})
        },
        synchronize_tooltip: function(columns) {
            var result = new Object();
            for (const item of columns) {
                result[item['id']] = {'value': item['name'], 'use_with': 'both'};
            }
            console.log(result);
            return result
        },
        open_sidebar:
        function(n_clicks, sidebar_status, open_text) {
            if (n_clicks) {
                if (!sidebar_status) {
                    return ['side-bar open', true, 'X'];
                }
                else {
                    return ['side-bar', false, '\u2630'];
                }
            }
            return 'side-bar', false;
        }
    }
})
