window.dash_clientside = Object.assign({}, window.dash_clientside, {
    modal: {
        open: function(trigger, is_open) {
            if (trigger) {
                return ~is_open;
            } else {
                return is_open
            }
        }
    }
});