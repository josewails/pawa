var chatMessages = [{
  name: "ms1",
  msg: "Who are you?",
  delay: 1000,
  align: "left",
  showTime: true,
  time: "19:58"
},
{
  name: "ms2",
  msg: "We are young team of entrepreneurs, developers, designers and visionaries. We are based in Berlin and started working on Freedactics in early 2015.",
  delay: 1000,
  align: "left",
  showTime: true,
  time: "19:58"
},
{
  name: "ms3",
  msg: "Could you describe Freedactics in one sentence?",
  delay: 3000,
  align: "right",
  showTime: true,
  time: "19:58"
},
{
  name: "ms4",
  msg: "Everything from lecture to exam in your pocket: Freedactics is a cloud-based platform build for students needs.",
  delay: 7000,
  align: "left",
  showTime: true,
  time: "19:58"
},
{
  name: "ms5",
  msg: "And the longer version?",
  delay: 3000,
  align: "right",
  showTime: true,
  time: "19:58"
},
{
  name: "ms6",
  msg: "As students we use to organize all our daily life around web and mobile technology, except the actual studying part. For learning we still use huge amounts of paper, books and heavy backpacks.",
  delay: 11000,
  align: "left",
  showTime: false,
  time: "19:58"
},
{
  name: "ms7",
  msg: "Why? Because there is no solution out there to help students or teachers to easily digitalize their learning processes and contents. We think that learning should be fast, simple and effective. A platform for studying should give people the option to learn at their own scope, with their own contents integrated.",
  delay: 10000,
  align: "left",
  showTime: false,
  time: "19:58"
},
{
  name: "ms8",
  msg: "This is why we developed Freedactics – a cloud-based solution tailored to students needs.",
  delay: 8000,
  align: "left",
  showTime: true,
  time: "19:58"
},
{
  name: "ms9",
  msg: "What makes you different from other learning platforms?",
  delay: 4000,
  align: "right",
  showTime: true,
  time: "19:58"
},
{
  name: "ms10",
  msg: "We understand the needs of individual student. We don’t focus so much on content publishing or learning management but on learning. At the same time we acknowledge the need to integrate different perspectives, such as flash cards, content and task management.",
  delay: 8000,
  align: "left",
  showTime: false,
  time: "19:58"
},
{
  name: "ms11",
  msg: "So we end up with a unique mix of focus on User Experience and thrive towards integration.",
  delay: 4000,
  align: "left",
  showTime: true,
  time: "19:58"
},
{
  name: "ms12",
  msg: "What is your vision for the future?",
  delay: 4000,
  align: "right",
  showTime: true,
  time: "19:58"
},
{
  name: "ms14",
  msg: "We are releasing an App right now. But that’s only breaking ground. In fact, we have something much bigger in mind: a universe of education! Our vision is to connect people, connect tools and power learning through intelligent systems.",
  delay: 9000,
  align: "left",
  showTime: true,
  time: "19:58"
},
{
  name: "ms15",
  msg: "Thanks! Something you want to add?",
  delay: 3000,
  align: "left",
  showTime: true,
  time: "19:58"
},
{
  name: "ms16",
  msg: "You are welcome! Yes, check out freedactics.com!",
  delay: 9000,
  align: "left",
  showTime: true,
  time: "19:58"
}
                   ];
var chatDelay = 0;

function onRowAdded() {
  $('.chat-container').animate({
    scrollTop: $('.chat-container').prop('scrollHeight')
  });
};
$.each(chatMessages, function(index, obj) {
  chatDelay = chatDelay + 4000;
  chatDelay2 = chatDelay + obj.delay;
  chatDelay3 = chatDelay2 + 10;
  scrollDelay = chatDelay;
  chatTimeString = " ";
  msgname = "." + obj.name;
  msginner = ".messageinner-" + obj.name;
  spinner = ".sp-" + obj.name;
  if (obj.showTime == true) {
    chatTimeString = "<span class='message-time'>" + obj.time + "</span>";
  }
  $(".chat-message-list").append("<li class='message-" + obj.align + " " + obj.name + "' hidden><div class='sp-" + obj.name + "'><span class='spinme-" + obj.align + "'><div class='spinner'><div class='bounce1'></div><div class='bounce2'></div><div class='bounce3'></div></div></span></div><div class='messageinner-" + obj.name + "' hidden><span class='message-text'>" + obj.msg + "</span>" + chatTimeString + "</div></li>");
  $(msgname).delay(chatDelay).fadeIn();
  $(spinner).delay(chatDelay2).hide(1);
  $(msginner).delay(chatDelay3).fadeIn();
  setTimeout(onRowAdded, chatDelay);
  setTimeout(onRowAdded, chatDelay3);
  chatDelay = chatDelay3;
});