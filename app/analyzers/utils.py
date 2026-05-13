import ast

def resolve_node_value(node, variables=None, project_context=None):

    variables = variables or {}
    project_context = project_context or {}
    if isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.Name):
        return (
            variables.get(node.id)
            or project_context.get(node.id)
        )
    elif isinstance(node, ast.BinOp):

        if isinstance(node.op, ast.Add):

            left = resolve_node_value(
                node.left,
                variables,
                project_context
            )

            right = resolve_node_value(
                node.right,
                variables,
                project_context
            )

            if left is not None and right is not None:
                return str(left) + str(right)

    return None