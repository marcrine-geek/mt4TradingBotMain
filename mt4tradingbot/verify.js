
const express = require('express')
const app = express()

app.use(express.json())

const { MTProto } = require('telegram-mtproto')

const phone = {
  num : '+254742253052',
  code: '22222'
}

const api = {
  layer          : 57,
  initConnection : 0x69796de9,
  api_id         : 49631
}

const server = {
  dev: true //We will connect to the test server.
}           //Any empty configurations fields can just not be specified

const client = MTProto({ server, api })


async function connect(phone, code){   

   
  const { phone_code_hash } = await client('auth.sendCode', {
    phone_number  : phone.num,
    current_number: false,
    api_id        : 49631,
    api_hash      : 'fb050b8f6771e15bfda5df2409931569'
  })
  

  setTimeout(connect, 30000)

    
    
  const { user } = await client('auth.signIn', {
    phone_number   : num.phone,
    phone_code_hash: phone_code_hash,
    phone_code     : phone.code
  })
  

  console.log('signed as ', user)
}

// async function mobileVerfy(phone){
//   const telegram = await client('auth.sendCode', {
//     phone_number  : phone,
//     current_number: false,
//     api_id        : 49631,
//     api_hash      : 'fb050b8f6771e15bfda5df2409931569'
//   })

//   return telegram;
// }

// setTimeout(mobileVerfy, 30000)

// async function codeVerification (phone,code) {
//   const { user } = await client('auth.signIn', {
//     phone_number   : phone,
//     phone_code     : code
//   })
// }
// // connect()

app.post('/', (req, res) => {
  const phone = req.body.phone

  connect(phone).then((response) => {
    res.send(response)
  })

})

app.post('/verify/code', (req, res) => {
  const code = req.body.code
  const phone = req.body.phone


  connect(phone, code).then((response) => {
    res.send(response)
  })
})

app.listen(6060, () => {
  console.log('server imestart');
})