from flask import jsonify

def register_routes(app):
    """
    Register all routes for the Flask app.
    """
    @app.route("/nodes", methods=["GET"])
    def list_nodes():
        """
        API endpoint to list all nodes.
        """
        return jsonify({"nodes": list(app.config["nodes"].keys())})

    @app.route('/nodes/<node_name>/power-on', methods=["GET", "POST"])
    def power_on_node(node_name):
        if node_name not in app.config["nodes"]:
            app.logger.warning("Node \"%s\" not found.", node_name)
            return jsonify({"error": "Node not found"}), 404
        node = app.config["nodes"][node_name]
        node.power_on()
        return jsonify({"status": "ok"})

    @app.route('/nodes/<node_name>/power-off', methods=["GET", "POST"])
    def power_off_node(node_name):
        if node_name not in app.config["nodes"]:
            app.logger.warning("Node \"%s\" not found.", node_name)
            return jsonify({"error": "Node not found"}), 404
        node = app.config["nodes"][node_name]
        node.power_off()
        return jsonify({"status": "ok"})

    @app.route('/nodes/<node_name>/state', methods=["GET", "POST"])
    def node_state(node_name):
        if node_name not in app.config["nodes"]:
            app.logger.warning("Node \"%s\" not found.", node_name)
            return jsonify({"error": "Node not found"}), 404
        node = app.config["nodes"][node_name]
        return jsonify({"state": node.power_state})
