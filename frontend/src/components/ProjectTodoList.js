import {useParams} from 'react-router-dom'


const TodoItem = ({todo}) => {
    return (
        <tr>
            <td>
                {todo.text}
            </td>
            <td>
                {todo.time}
            </td>
            <td>
                {todo.author}
            </td>
        </tr>
    )
}


const ProjectTodoList = ({todos}) => {
    var {id} = useParams()
    var filteredTodos = todos.filter((todo) => todo.text.includes(parseInt(id)))

    return (
        <table>
            <th>
                Text
            </th>
            <th>
                Time
            </th>
            <th>
                Authors
            </th>
            {filteredTodos.map((todo) => <TodoItem todo={todo} />)}
        </table>
    )
}

export default ProjectTodoList