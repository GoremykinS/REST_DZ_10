import {Link} from 'react-router-dom'


const UserItem = ({user}) => {
    return (
        <tr>
            <td>
                {user.age}
            </td>
            <td>
                <Link to={`/user/${user.id}`} >{user.city}</Link>
            </td>

            <td>
                {user.user_name}

            </td>
        </tr>
    )
}


const UserList = ({users}) => {
    return (
        <table>
            <th>
                Age
            </th>
            <th>
                City
            </th>
            <th>
               User_name
            </th>
            {users.map((user) => <UserItem user={user} />)}
        </table>
    )
}

export default UserList