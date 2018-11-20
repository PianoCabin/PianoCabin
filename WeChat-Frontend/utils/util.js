const formatTime = date => {
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hour = date.getHours()
  const minute = date.getMinutes()
  const second = date.getSeconds()

  return [year, month, day].map(formatNumber).join('/') + ' ' + [hour, minute, second].map(formatNumber).join(':')
}

const msgPrompt = msg => {
  wx.showToast({
    title: msg,
    icon: 'success',
    duration: 1000,
    mask: true
  })
}

const formatNumber = n => {
  n = n.toString()
  return n[1] ? n : '0' + n
}


const timeStringToTimestamp = (cur_date_str, time_str) => {
  let date = new Date(cur_date_str)
  let list = time_str.split(":");
  date.setHours(parseInt(list[0]), parseInt(list[1]), 0, 0);
  return date.getTime();
}

const timestamptoTimeString = stamp => {
  let date = new Date(stamp);
  return date.getHours().toString() + ':' + date.getMinutes().toString()
}

const timestampToDateString = stamp => {
  let date = new Date(stamp);
  return date.getFullYear().toString() + '/' + (date.getMonth() + 1).toString() + '/' + date.getDate().toString();
}


module.exports = {
  formatTime: formatTime,
  msgPrompt: msgPrompt,
  timeStringToTimestamp: timeStringToTimestamp,
  timestampToTimeString: timestamptoTimeString,
  timestampToDateString: timestampToDateString,
}
