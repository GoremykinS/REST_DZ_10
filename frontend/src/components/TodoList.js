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


const TodoList = ({todos}) => {
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
            {todos.map((todo) => <TodoItem todo={todo} />)}
        </table>
    )
}

export default TodoList